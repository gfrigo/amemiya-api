from base64 import b64encode

from src.core.config import logger
from src.endpoints import generic_repository
from .queries import AssembleStatement


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

        try:
            insert_stmt = AssembleStatement.add_user(tuple(data.keys()), tuple(data.values()))
            logger.info(f"To execute: {insert_stmt}")

            cursor.execute(insert_stmt)
            logger.info("Executed")

        except Exception as e:
            print(e)
            return None

        return cursor.lastrowid

    @staticmethod
    def edit(cursor, data: dict):
        logger.info("EDIT USER REPOSITORY HIT")

        try:
            update_stmt = generic_repository.edit(data)
            logger.info(f"To execute: {update_stmt}")

            cursor.execute(update_stmt)
            logger.info("Executed")

        except Exception as e:
            logger.info("Error during edit:", e)

    @staticmethod
    def remove(cursor, data: dict):
        logger.info("REMOVE USER REPOSITORY HIT")

        try:
            remove_stmt = generic_repository.remove(data)
            logger.info(f"To execute: {remove_stmt}")

            cursor.execute(remove_stmt)
            logger.info("Executed")

        except Exception as e:
            logger.info("Error during remotion:", e)

