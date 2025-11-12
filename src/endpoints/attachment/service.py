from src.core.config import settings
from src.core.database import start_connection, start_cursor
from src.core.config import logger
from src.endpoints import generic_repository
from .model import AttachmentDataRequest
from .repository import AttachmentRepository


def fetch_attachment_service(company_id: int,
                             user_id: int | None = None,
                             attachment_type: str | None = None,
                             date_range_start: str | None = None,
                             date_range_end: str | None = None) -> dict:

    logger.info("FETCH ATTACHMENT SERVICE HIT")

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

    with start_connection(settings.db_credentials) as conn:
        with start_cursor(conn) as cursor:

            result: dict = AttachmentRepository.fetch(cursor, query_filter)

    return result

def add_attachment_service(request_data: dict):
    logger.info("ADD ATTACHMENT SERVICE HIT")

    request_data = {k: v for k, v in request_data.items() if v is not None}

    with start_connection(settings.db_credentials) as conn:
        with start_cursor(conn) as cursor:

            attachment_id: int = AttachmentRepository.add(cursor, request_data)

        conn.commit()

    if attachment_id:
        return attachment_id

    else:
        return None

def edit_attachment_service(request_data: dict):
    logger.info("EDIT ATTACHMENT SERVICE HIT")

    request_data = {k: v for k, v in request_data.items() if v is not None}

    request_attachment_id: int = request_data.get("attachment_id")

    query_filter = {
        "table": "Attachments",
        "attachment_id": {"type": "index",
                          "value": request_attachment_id,
                          "table": "Attachments"}
    }

    query_data = {
        "table": "Attachments",
        "filter": query_filter,
        "data": request_data
    }

    with start_connection(settings.db_credentials) as conn:
        with start_cursor(conn) as cursor:

            attachment_data: dict = AttachmentRepository.fetch(cursor, query_filter)

            if not attachment_data:
                raise IndexError("Attachment ID has no data")

            AttachmentRepository.edit(cursor, query_data)

        conn.commit()

def remove_attachment_service(attachment_id: int):
    logger.info("REMOVE ATTACHMENT SERVICE HIT")

    query_filter = {
        "table": "Attachments",
        "attachment_id": {"type": "index",
                          "value": attachment_id,
                          "table": "Attachments"}
    }

    query_data = {
        "table": "Attachments",
        "filter": query_filter
    }

    with start_connection(settings.db_credentials) as conn:
        with start_cursor(conn) as cursor:
            attachment_data: dict = AttachmentRepository.fetch(cursor, query_filter)

            if not attachment_data:
                raise IndexError("Attachment ID has no data")

            AttachmentRepository.remove(cursor, query_data)

        conn.commit()
