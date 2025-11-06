from src.core.logging_config import logger
from src.core.database import start_connection, start_cursor
from src.endpoints.user.repository import UserRepository
from src.endpoints.user.model import UserDataRequest
from src.core.utils import check_missing_fields
from src.core.config import settings


def fetch_user_service(request_data: dict) -> dict | list:
    logger.info("FETCH USER SERVICE HIT")

    request_company_id: int = request_data["company_id"]
    request_user_id: int = request_data["user_id"]

    query_filter = {
        "company_id": {"type": "index",
                       "value": request_company_id,
                       "table": "Users"},
        "user_id": {"type": "index",
                    "value": request_user_id,
                    "table": "Users"}
    }

    with start_connection(settings.DB_HOST, settings.DB_USER, settings.DB_PASSWORD, settings.DB_SCHEMA) as conn:
        with start_cursor(conn) as cursor:
            result: dict | list = UserRepository.fetch(cursor, query_filter)

            return result

def add_user_service(request_data: dict):
    logger.info("ADD USER SERVICE HIT")

    request_data = {k: v for k, v in request_data.items() if v is not None}

    with start_connection(settings.DB_HOST, settings.DB_USER, settings.DB_PASSWORD, settings.DB_SCHEMA) as conn:
        with start_cursor(conn) as cursor:

            user_id: int = UserRepository.add(cursor, request_data)

        conn.commit()

    if user_id:
        return user_id

    else:
        return None

def edit_user_service(request_data: dict):
    logger.info("EDIT USER SERVICE HIT")

    request_data = {k: v for k, v in request_data.items() if v is not None}

    request_company_id: int = request_data.get("company_id")
    request_user_id: int = request_data.get("user_id")

    query_filter = {
        "company_id": {"type": "index",
                       "value": request_company_id,
                       "table": "Users"},
        "user_id": {"type": "index",
                    "value": request_user_id,
                    "table": "Users"}
    }

    query_data = {
        "table": "Users",
        "filter": query_filter,
        "data": request_data
    }

    with start_connection(settings.DB_HOST, settings.DB_USER, settings.DB_PASSWORD, settings.DB_SCHEMA) as conn:
        with start_cursor(conn) as cursor:

            user_data: dict = UserRepository.fetch(cursor, query_filter)

            if not user_data:
                return "user_id has no data"

            UserRepository.edit(cursor, query_data)

        conn.commit()

    return "User edited successfully"

def remove_user_service(request_data: dict):
    logger.info("REMOVE USER SERVICE HIT")

    request_user_id: int = request_data.get("user_id")

    query_filter = {
        "user_id": {"type": "index",
                    "value": request_user_id,
                    "table": "Users"}
    }

    query_data = {
        "table": "Users",
        "filter": query_filter
    }

    with start_connection(settings.DB_HOST, settings.DB_USER, settings.DB_PASSWORD, settings.DB_SCHEMA) as conn:
        with start_cursor(conn) as cursor:
            user_data: dict = UserRepository.fetch(cursor, query_filter)
            if not user_data:
                return "user_id has no data"

            UserRepository.remove(cursor, query_data)

        conn.commit()

    return "User removed successfully"