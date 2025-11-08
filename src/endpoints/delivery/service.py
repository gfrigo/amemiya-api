from src.core.logging_config import logger
from src.core.database import start_connection, start_cursor
from .repository import RouteRepository
from .model import DeliveryDataRequest
from src.endpoints import generic_repository
from src.core.utils import check_missing_fields
from src.core.config import settings


def fetch_delivery_service(delivery_id: int,
                             vehicle_id: int | None = None,
                             route_id: int | None = None,
                             finish_time: str | None = None,
                             load_name: str | None = None,
                             start_time: str | None = None) -> dict:

    logger.info("FETCH DELIVERY SERVICE HIT")

    query_filter = {
            "delivery_id": {"type": "index",
                                       "value": delivery_id,
                                       "table": "Delivery"},
            "route_id": {"type": "index",
                                    "value": route_id,
                                    "table": "Delivery"},
            "vehicle_id": {"type": "index",
                                    "value": vehicle_id,
                                    "table": "Delivery"},
            "load_name": {"type": "index",
                                "value": load_name,
                                "table": "Delivery"},
            "upload_date": {"type": "date_range",
                            "value": (start_time, finish_time),
                            "table": "Delivery"}
    }

    with start_connection(settings.DB_HOST, settings.DB_USER, settings.DB_PASSWORD, settings.DB_SCHEMA) as conn:
        with start_cursor(conn) as cursor:

            result: dict = RouteRepository.fetch(cursor, query_filter)

    return result

def add_delivery_service(data: dict):
    logger.info("ADD DELIVERY SERVICE HIT")

    delivery_data: dict = data

    with start_connection(settings.DB_HOST, settings.DB_USER, settings.DB_PASSWORD, settings.DB_SCHEMA) as conn:
        with start_cursor(conn) as cursor:

            delivery_id = RouteRepository.add(cursor, data)
            conn.commit()

    if delivery_id:
        return "Route added successfully"

    else:
        return "Route creation failed"

def edit_attachment_service(attachment_id: int, request: DeliveryDataRequest):
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
