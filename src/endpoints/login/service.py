from src.core.database import start_connection, start_cursor
from .repository import LoginRepository
from .model import LoginDataRequest
from src.core.config import settings
from src.core.utils import check_missing_fields


def fetch_login_service(request: LoginDataRequest) -> tuple:
    data = request.model_dump()
    required_fields = ["email", "password"]
    check_missing_fields(data, required_fields)

    with start_connection(settings.DB_HOST, settings.DB_USER, settings.DB_PASSWORD, settings.DB_SCHEMA) as conn:
        with start_cursor(conn) as cursor:

            access = LoginRepository.get_access(cursor, data["email"], data["password"])
            user_id = access[1]
            print(user_id)
            user_data = LoginRepository.get_user_data(cursor, user_id)

            return user_data

