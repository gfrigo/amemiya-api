from src.core.database import start_connection, start_cursor
from .repository import LoginRepository
from .schema import LoginDataRequest
from src.core.config import settings
from src.core.utils import check_missing_fields


def fetch_login_service(request: LoginDataRequest, conn = None, cursor = None) -> dict:
    data = request.model_dump()
    required_fields = ["email", "password"]
    check_missing_fields(data, required_fields)

    with start_connection(settings.DB_HOST, settings.DB_USER, settings.DB_PASSWORD, settings.DB_SCHEMA) as conn:
        with start_cursor(conn) as cursor:

            access = LoginRepository.get_access(cursor, data["email"], data["password"])
            user_data = LoginRepository.get_user_data(cursor, access["user_id"])

            return user_data

