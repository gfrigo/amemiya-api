from src.core.logging_config import logger
from src.register import Register
from src.core.database import Execute
from src.queries import user_queries
from base64 import b64encode


class UserRepository:

    @staticmethod
    def fetch(cursor, data: dict) -> dict | None:
        logger.info("FETCH USER REPOSITORY HIT")
        company_id: int = data.get("company_id")
        user_id: int = data.get("user_id")

        if not company_id:
            return None

        users_data = Execute.Select.from_string(cursor, user_queries.User.get_data(company_id))

        if user_id:
            user_data = (x for x in users_data if x[0] == user_id)

            try:

                print(user_data)

                user_id, user_name, inner_register, _, email, telephone, role_id, role_name, admin, company_id, company_name, picture_data, picture_type, active_user = user_data

                encoded_picture_data = b64encode(picture_data).decode("utf-8")

                return {
                    "user_id": user_id,
                    "user_name": user_name,
                    "inner_register": inner_register,
                    "email": email,
                    "telephone": telephone,
                    "role_name": role_name,
                    "admin": True if admin == 1 else False,
                    "company_name": company_name,
                    "profile_picture": encoded_picture_data,
                    "active_user": active_user
                }

            except IndexError:
                return None

        else:
            users = {}
            for x in users_data:
                user_id, user_name, inner_register, _, email, telephone, role_id, role_name, admin, company_id, company_name, picture_data, picture_type, active_user = x
                encoded_picture_data = b64encode(picture_data).decode("utf-8")
                users[user_id] = {
                    "user_id": user_id,
                    "user_name": user_name,
                    "inner_register": inner_register,
                    "email": email,
                    "telephone": telephone,
                    "role_name": role_name,
                    "admin": True if admin == 1 else False,
                    "company_name": company_name,
                    "profile_picture": encoded_picture_data,
                    "active_user": active_user
                }
            return users

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

