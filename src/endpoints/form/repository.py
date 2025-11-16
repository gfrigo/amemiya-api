from base64 import b64encode

from src.core.config import logger
from src.endpoints import generic_repository
from .queries import AssembleStatement


class FormRepository:

    @staticmethod
    def fetch(cursor, query_filter: dict) -> dict | list | None:
        logger.info("FETCH USER REPOSITORY HIT")

        try:
            select_stmt = AssembleStatement.get_form_data(query_filter)
            logger.info(f"To execute: {select_stmt}")

            cursor.execute(select_stmt)
            logger.info("Executed")

            result = cursor.fetchall()

            if not result:
                return None

            data: list = []
            for entry in result:
                (
                    form_id,
                    company_id,
                    company_name,
                    user_id,
                    user_name,
                    delivery_id,
                    delivery_code,
                    description,
                    was_delivered,
                    had_problem,
                    problem_description,
                    who_received,
                    creation_datetime,
                    notes
                ) = entry

                data.append({
                    "form_id": form_id,
                    "company_id": company_id,
                    "company_name": company_name,
                    "user_id": user_id,
                    "user_name": user_name,
                    "delivery_id": delivery_id,
                    "delivery_code": delivery_code,
                    "description": description,
                    "was_delivered": was_delivered == 1,
                    "had_problem": had_problem == 1,
                    "problem_description": problem_description,
                    "who_received": who_received,
                    "creation_datetime": str(creation_datetime),
                    "notes": notes
                })

            return data

        except IndexError:
            return None

        except ValueError:
            return None


    @staticmethod
    def add(cursor, data: dict):
        logger.info("ADD FORM REPOSITORY HIT")

        try:
            insert_stmt = AssembleStatement.add_form(tuple(data.keys()), tuple(data.values()))
            logger.info(f"To execute: {insert_stmt}")

            cursor.execute(insert_stmt)
            logger.info("Executed")

        except Exception as e:
            print(e)
            return None

        return cursor.lastrowid

    @staticmethod
    def edit(cursor, data: dict):
        logger.info("EDIT FORM REPOSITORY HIT")

        try:
            update_stmt = generic_repository.edit(data)
            logger.info(f"To execute: {update_stmt}")

            cursor.execute(update_stmt)
            logger.info("Executed")


        except Exception as e:
            logger.info("Error during edition:", e)

    @staticmethod
    def remove(cursor, data: dict):
        logger.info("REMOVE FORM REPOSITORY HIT")

        try:
            remove_stmt = generic_repository.remove(data)
            logger.info(f"To execute: {remove_stmt}")

            cursor.execute(remove_stmt)
            logger.info("Executed")

        except Exception as e:
            logger.info("Error during remotion:", e)

