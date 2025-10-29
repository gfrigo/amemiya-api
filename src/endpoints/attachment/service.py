from src.core.logging_config import logger
from src.core.database import start_connection, start_cursor
from .repository import AttachmentRepository
from .model import AttachmentDataRequest
from src.core.utils import check_missing_fields
from src.core.config import settings


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

    with start_connection(settings.DB_HOST, settings.DB_USER, settings.DB_PASSWORD, settings.DB_SCHEMA) as conn:
        with start_cursor(conn) as cursor:

            result: dict = AttachmentRepository.fetch(cursor, query_filter)

    return result

def add_attachment_service(data):
    logger.info("ADD ATTACHMENT SERVICE HIT")

    with start_connection(settings.DB_HOST, settings.DB_USER, settings.DB_PASSWORD, settings.DB_SCHEMA) as conn:
        with start_cursor(conn) as cursor:

            AttachmentRepository.add(cursor, data.dict())
            conn.commit()

    return "User added successfully"

def edit_user_service(request: AttachmentDataRequest, conn = None, cursor = None):
    logger.info("EDIT USER SERVICE HIT")
    data = request.model_dump()
    required_fields = ["user_id"]
    check_missing_fields(data, required_fields)

    with start_connection(settings.DB_HOST, settings.DB_USER, settings.DB_PASSWORD, settings.DB_SCHEMA) as conn:
        with start_cursor(conn) as cursor:
            user_data: dict = AttachmentRepository.fetch(cursor, data)
            if not user_data:
                return "user_id has no data"

            AttachmentRepository.edit(cursor, data)
            conn.commit()
    return "User edited successfully"

def remove_user_service(request: AttachmentDataRequest, conn = None, cursor = None):
    logger.info("REMOVE USER SERVICE HIT")
    data = request.model_dump()
    required_fields = ["user_id"]
    check_missing_fields(data, required_fields)

    with start_connection(settings.DB_HOST, settings.DB_USER, settings.DB_PASSWORD, settings.DB_SCHEMA) as conn:
        with start_cursor(conn) as cursor:
            user_data: dict = AttachmentRepository.fetch(cursor, data)
            if not user_data:
                return "user_id has no data"

            AttachmentRepository.remove(cursor, data)
            conn.commit()
    return "User removed successfully"