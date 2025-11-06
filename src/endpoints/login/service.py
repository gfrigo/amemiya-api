from src.core.database import start_connection, start_cursor
from .repository import LoginRepository
from src.core.config import settings
from src.core.logging_config import logger


def fetch_login_service(request_data: dict) -> tuple:
    logger.info("FETCH LOGIN SERVICE HIT")

    request_email: str = request_data["email"]
    request_password: str = request_data["password"]

    query_filter = {
        "email": {"type": "index",
                  "value": request_email,
                  "table": "Users"},
        "password": {"type": "index",
                     "value": request_password,
                     "table": "Users"},
        "active_user": {"type": "index",
                        "value": 1,
                        "table": "Users"}
    }

    with start_connection(settings.DB_HOST, settings.DB_USER, settings.DB_PASSWORD, settings.DB_SCHEMA) as conn:
        with start_cursor(conn) as cursor:

            access, user_data = LoginRepository.fetch(cursor, query_filter)

            return access, user_data