from .queries import AssembleStatement
from src.core.logging_config import logger
from base64 import b64encode


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

            user_id, user_name, inner_register, email, telephone, role_id, role_name, admin, company_id, company_name, profile_picture_id, profile_picture_data = result

            encoded_picture_data = b64encode(profile_picture_data).decode("utf-8")

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
                "profile_picture_data": encoded_picture_data
            }

            return True, data

        except IndexError:
            return False, None