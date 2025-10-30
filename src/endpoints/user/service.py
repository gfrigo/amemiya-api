from src.core.logging_config import logger
from src.core.database import start_connection, start_cursor
from src.endpoints.user.repository import UserRepository
from src.endpoints.user.model import UserDataRequest
from src.core.utils import check_missing_fields
from src.core.config import settings


def fetch_user_service(request: UserDataRequest, conn = None, cursor = None) -> dict:
    logger.info("FETCH USER SERVICE HIT")
    data = request.model_dump()
    required_fields = ["user_id"]
    check_missing_fields(data, required_fields)

    with start_connection(settings.DB_HOST, settings.DB_USER, settings.DB_PASSWORD, settings.DB_SCHEMA) as conn:
        with start_cursor(conn) as cursor:
            result: dict = UserRepository.fetch(cursor, data)
            return result

def add_user_service(request: UserDataRequest, conn = None, cursor = None):
    logger.info("ADD USER SERVICE HIT")
    data = request.model_dump()
    required_fields = ["user_name", "password", "email", "telephone", "role_id", "company_id"]
    check_missing_fields(data, required_fields)

    with start_connection(settings.DB_HOST, settings.DB_USER, settings.DB_PASSWORD, settings.DB_SCHEMA) as conn:
        with start_cursor(conn) as cursor:
            UserRepository.add(cursor, data)
            conn.commit()

    return "User added successfully"

def edit_user_service(request: UserDataRequest | dict, conn = None, cursor = None):
    logger.info("EDIT USER SERVICE HIT")

    if not isinstance(request, dict):
        data = request.model_dump()
        required_fields = ["user_id"]
        check_missing_fields(data, required_fields)

    else:
        data = request

    with start_connection(settings.DB_HOST, settings.DB_USER, settings.DB_PASSWORD, settings.DB_SCHEMA) as conn:
        with start_cursor(conn) as cursor:
            user_data: dict = UserRepository.fetch(cursor, data)
            if not user_data:
                return "user_id has no data"

            UserRepository.edit(cursor, data)
            conn.commit()

    return "User edited successfully"

def remove_user_service(request: UserDataRequest, conn = None, cursor = None):
    logger.info("REMOVE USER SERVICE HIT")
    data = request.model_dump()
    required_fields = ["user_id"]
    check_missing_fields(data, required_fields)

    with start_connection(settings.DB_HOST, settings.DB_USER, settings.DB_PASSWORD, settings.DB_SCHEMA) as conn:
        with start_cursor(conn) as cursor:
            user_data: dict = UserRepository.fetch(cursor, data)
            if not user_data:
                return "user_id has no data"

            UserRepository.remove(cursor, data)
            conn.commit()
    return "User removed successfully"