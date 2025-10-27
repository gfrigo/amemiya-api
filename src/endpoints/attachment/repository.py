from .queries import get_data
from src.core.logging_config import logger
from src.register import Register



class AttachmentRepository:

    @staticmethod
    def fetch(cursor, query_filter: dict) -> dict | None:
        logger.info("FETCH ATTACHMENT REPOSITORY HIT")

        try:
            select_stmt = get_data(query_filter)

            cursor.execute(select_stmt)
            result = cursor.fetchall()

            if not result:
                return None

            # TODO
            return {}

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

