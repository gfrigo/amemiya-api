from src.core.logging_config import logger
from src.register import Register
from src.core.database import Execute
from src.queries import user_queries
from base64 import b64encode


class UserRepository:

    @staticmethod
    def fetch(cursor, data: dict) -> dict | None:
        logger.info("FETCH USER REPOSITORY HIT")
        user_id: int = data["user_id"]

        if not user_id:
            return None

        user_data = Execute.Select.from_string(cursor, user_queries.User.get_data(user_id))[0]

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

