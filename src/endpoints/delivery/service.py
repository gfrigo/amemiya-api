from src.core.logging_config import logger
from src.core.database import start_connection, start_cursor
from .repository import RouteRepository
from .model import DeliveryDataRequest
from src.endpoints import generic_repository
from src.core.utils import check_missing_fields
from src.core.config import settings


def fetch_delivery_service(company_id: int,
                             user_id: int | None = None,
                             attachment_type: str | None = None,
                             date_range_start: str | None = None,
                             date_range_end: str | None = None) -> dict:

    logger.info("FETCH DELIVERY SERVICE HIT")

    query_filter = {
            "uploaded_by_company_id": {"type": "index",
                                       "value": company_id,
                                       "table": "Attachments"},
            "uploaded_by_user_id": {"type": "index",
                                    "value": user_id,
                                    "table": "Attachments"},
            "attachment_type": {"type": "index",
                                "value": attachment_type,
                                "table": "Attachments"},
            "upload_date": {"type": "date_range",
                            "value": (date_range_start, date_range_end),
                            "table": "Attachments"}
    }

    with start_connection(settings.DB_HOST, settings.DB_USER, settings.DB_PASSWORD, settings.DB_SCHEMA) as conn:
        with start_cursor(conn) as cursor:

            result: dict = RouteRepository.fetch(cursor, query_filter)

    return result

def add_route_service(data: dict):
    logger.info("ADD ROUTE SERVICE HIT")

    route_data: dict = data
    subroutes: list = route_data.pop("subroutes")

    subroutes_data: dict = {}
    for idx, entry in enumerate(subroutes):
        entry_data = list(entry.values())
        subroutes_data[idx+1] = {
            "subroute_type": entry_data[0],
            "address": entry_data[1],
            "longitude": entry_data[2],
            "latitude": entry_data[3]
        }

    route_data["subroutes"] = subroutes_data

    with start_connection(settings.DB_HOST, settings.DB_USER, settings.DB_PASSWORD, settings.DB_SCHEMA) as conn:
        with start_cursor(conn) as cursor:

            route_id = RouteRepository.add(cursor, data)
            conn.commit()

    if route_id:
        return "Route added successfully"

    else:
        return "Route creation failed"

def edit_attachment_service(attachment_id: int, request: RouteDataRequest):
    logger.info("EDIT ATTACHMENT SERVICE HIT")
    data = request.model_dump()

    query_filter = {
        "attachment_id": {"type": "index",
                          "value": attachment_id,
                          "table": "Attachments"}
    }

    with start_connection(settings.DB_HOST, settings.DB_USER, settings.DB_PASSWORD, settings.DB_SCHEMA) as conn:
        with start_cursor(conn) as cursor:

            attachment_data: dict = RouteRepository.fetch(cursor, query_filter)

            if not attachment_data:
                raise IndexError("Attachment ID has no data")

            RouteRepository.edit(cursor, attachment_id, data)
            conn.commit()

def remove_attachment_service(attachment_id: int):
    logger.info("REMOVE ATTACHMENT SERVICE HIT")

    query_filter = {
        "table": "Attachments",
        "attachment_id": {"type": "index",
                          "value": attachment_id,
                          "table": "Attachments"}
    }

    with start_connection(settings.DB_HOST, settings.DB_USER, settings.DB_PASSWORD, settings.DB_SCHEMA) as conn:
        with start_cursor(conn) as cursor:
            attachment_data: dict = RouteRepository.fetch(cursor, query_filter)

            if not attachment_data:
                raise IndexError("Attachment ID has no data")

            generic_repository.remove(cursor, query_filter)
            conn.commit()
