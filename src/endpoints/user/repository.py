from src.core.logging_config import logger
from src.register import Register
from src.core.database import Execute
from src.queries import user_queries
from .queries import AssembleStatement
from base64 import b64encode


class UserRepository:

    @staticmethod
    def fetch(cursor, query_filter: dict) -> dict | list | None:
        logger.info("FETCH USER REPOSITORY HIT")
        request_user_id = query_filter["user_id"]["value"]

        try:

            if not request_user_id:
                select_stmt = AssembleStatement.get_all_users(query_filter)

            else:
                select_stmt = AssembleStatement.get_user_data(query_filter)

            logger.info(f"To execute: {select_stmt}")

            cursor.execute(select_stmt)
            logger.info("Executed")

            result = cursor.fetchall()

            if not request_user_id:
                users_data: list = []

                users = result
                for user_entry in users:
                    user_id, user_name, inner_register, email, telephone, role_id, role_name, company_id, company_name = user_entry

                    users_data.append({
                        "user_id": user_id,
                        "user_name": user_name,
                        "inner_register": inner_register,
                        "email": email,
                        "telephone": telephone,
                        "role_id": role_id,
                        "role_name": role_name,
                        "company_id": company_id,
                        "company_name": company_name
                    })

                return users_data

            else:
                user_data: dict = {}

                user_entry = result[0]

                user_id, user_name, inner_register, email, telephone, role_id, role_name, admin, company_id, company_name, profile_picture_id, profile_picture_data = user_entry

                encoded_picture_data = b64encode(profile_picture_data).decode("utf-8")

                user_data = {
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

                return user_data

        except IndexError:
            return None

        except ValueError:
            return None


    @staticmethod
    def add(cursor, data: dict):
        logger.info("ADD USER REPOSITORY HIT")

        Register.add(cursor, "user", (
            data["user_name"],
            data["inner_register"],
            data["password"],
            data["email"],
            data["telephone"],
            str(data["role_id"]),
            data["admin"] if data["admin"] else '0',
            str(data["company_id"]),
            None,
            '1'
        ))

    @staticmethod
    def edit(cursor, data: dict):
        logger.info("EDIT USER REPOSITORY HIT")

        print(data)

        Register.edit(cursor, "user", data, f"user_id = {data['user_id']}")

    @staticmethod
    def remove(cursor, data: dict):
        logger.info("REMOVE USER REPOSITORY HIT")

        Register.remove(cursor, "user", f"user_id = {data['user_id']}")

