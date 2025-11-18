from base64 import b64encode

from src.core.config import logger
from .queries import AssembleStatement


class LoginRepository:

    @staticmethod
    def fetch(cursor, query_filter: dict) -> tuple: # (access, user_data)
        logger.info("FETCH LOGIN REPOSITORY HIT")

        try:
            select_stmt = AssembleStatement.get_user_data(query_filter)
            logger.info(f"To execute: {select_stmt}")

            cursor.execute(select_stmt)
            logger.info("Executed")

            result = cursor.fetchone()

            if not result:
                return False, None

            # result now includes password after email
            user_id, user_name, inner_register, email, password_hash, telephone, role_id, role_name, admin, company_id, company_name, profile_picture_id, profile_picture_data = result

            encoded_picture_data = b64encode(profile_picture_data).decode("utf-8") if profile_picture_data else None

            data = {
                "user_id": user_id,
                "user_name": user_name,
                "inner_register": inner_register,
                "email": email,
                "telephone": telephone,
                "role_id": role_id,
                "role_name": role_name,
                "admin": admin == 1,
                "company_id": company_id,
                "company_name": company_name,
                "profile_picture_id": profile_picture_id,
                "profile_picture_data": encoded_picture_data,
                "password_hash": password_hash
            }

            return True, data

        except IndexError:
            return False, None