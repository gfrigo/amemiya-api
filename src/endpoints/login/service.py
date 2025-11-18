from src.core.config import logger
from src.core.config import settings
from src.core.database import start_connection, start_cursor
from .repository import LoginRepository


def fetch_login_service(request_data: dict) -> tuple:
    logger.info("FETCH LOGIN SERVICE HIT")

    request_email: str = request_data["email"]
    request_password: str = request_data["password"]

    # Only filter by email and active_user; password validation is done in service
    query_filter = {
        "email": {"type": "index",
                  "value": request_email,
                  "table": "Users"},
        "active_user": {"type": "index",
                        "value": 1,
                        "table": "Users"}
    }

    with start_connection(settings.db_credentials) as conn:
        with start_cursor(conn) as cursor:
            access, user_data = LoginRepository.fetch(cursor, query_filter)

            if not access or not user_data:
                return False, None, None

            # Extract stored password (may be plaintext or hashed)
            stored = user_data.get("password_hash")

            # verify
            from src.core.auth import verify_password, hash_password, create_access_token

            if not stored:
                return False, None, None

            # If stored password does not look like a bcrypt hash (starts with $2b$ or $2a$),
            # compare plaintext and migrate to hashed password if match.
            needs_rehash = False
            is_hashed = isinstance(stored, str) and stored.startswith("$2")

            if is_hashed:
                valid = verify_password(request_password, stored)
            else:
                # plaintext in DB - try direct comparison
                valid = (request_password == stored)
                if valid:
                    needs_rehash = True

            if not valid:
                return False, None, None

            # Remove password from returned user_data before returning to client
            user_data.pop("password_hash", None)

            # If necessary, update DB with hashed password
            if needs_rehash:
                new_hash = hash_password(request_password)
                try:
                    update_stmt = "UPDATE Users SET password = %s WHERE user_id = %s"
                    cursor.execute(update_stmt, (new_hash, user_data["user_id"]))
                    conn.commit()
                except Exception as e:
                    logger.error(f"Failed to re-hash password for user {user_data.get('user_id')}: {e}")

            # Create token
            token = create_access_token({"user_id": user_data["user_id"], "company_id": user_data.get("company_id")})

            return True, user_data, token