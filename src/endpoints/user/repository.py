from src.core.logging_config import logger
from src.register import Register


class UserRepository:

    @staticmethod
    def fetch(cursor, data: dict) -> dict | None:
        logger.info("FETCH USER REPOSITORY HIT")
        user_id: int = data["user_id"]

        if not user_id:
            return None

        filter_stmt: str = f"user_id = {user_id}"

        try:
            result: list = Register.fetch(cursor, "user", filter_stmt)[0]

            print(result)

            return {
                "user_id": result[0],
                "user_name": result[1],
                "inner_register": result[2],
                "password": result[3],
                "email": result[4],
                "telephone": result[5],
                "role_id": result[6],
                "admin": result[7],
                "company_id": result[8],
                "image_path": result[9],
                "active_user": result[10]
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
            data["image_path"] or 'assets/profiles/default.png',
            '1'
        ))

    @staticmethod
    def edit(cursor, data: dict):
        logger.info("EDIT USER REPOSITORY HIT")

        Register.edit(cursor, "user", data, f"user_id = {data['user_id']}")

    @staticmethod
    def remove(cursor, data: dict):
        logger.info("REMOVE USER REPOSITORY HIT")

        Register.remove(cursor, "user", f"user_id = {data['user_id']}")

