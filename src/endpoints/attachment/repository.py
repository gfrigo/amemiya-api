from base64 import b64encode

from src.core.config import logger
from src.endpoints import generic_repository
from .queries import AssembleStatement


class AttachmentRepository:

    @staticmethod
    def fetch(cursor, query_filter: dict) -> dict | list | None:
        logger.info("FETCH ATTACHMENT REPOSITORY HIT")

        try:
            select_stmt = AssembleStatement.get_attachment_data(query_filter)
            logger.info(f"To execute: {select_stmt}")

            cursor.execute(select_stmt)
            logger.info("Executed")

            result = cursor.fetchall()

            if not result:
                return None

            data: list = []
            for entry in result:
                attachment_id, company_name, user_name, file_data, file_type, attachment_type, upload_date = entry

                encoded_file_data = b64encode(file_data).decode("utf-8")

                file_name = f"test_output.{file_type}"
                with open(file_name, "wb") as f:
                    f.write(file_data)

                data.append({
                    "company_name": company_name,
                    "user_name": user_name,
                    "file_data": encoded_file_data,
                    "file_type": file_type,
                    "attachment_type": attachment_type,
                    "upload_date": upload_date
                })

            return data

        except IndexError:
            return None


    @staticmethod
    def add(cursor, data: dict):
        logger.info("ADD ATTACHMENT REPOSITORY HIT")

        try:

            insert_stmt = AssembleStatement.add_attachment(data)
            logger.info(f"To execute: {insert_stmt}")

            cursor.execute(insert_stmt, tuple(data.values()))
            logger.info("Executed")

        except Exception as e:
            print(e)
            return None

        return cursor.lastrowid


    @staticmethod
    def edit(cursor, data: dict):
        logger.info("EDIT ATTACHMENT REPOSITORY HIT")

        try:
            update_stmt = generic_repository.edit(data)
            logger.info(f"To execute: {update_stmt}")

            cursor.execute(update_stmt)
            logger.info("Executed")

        except Exception as e:
            print(e)
            return None


    @staticmethod
    def remove(cursor, data: dict):
        logger.info("REMOVE ATTACHMENT REPOSITORY HIT")

        try:
            remove_stmt = generic_repository.remove(data)
            logger.info(f"To execute: {remove_stmt}")

            cursor.execute(remove_stmt)
            logger.info("Executed")

        except Exception as e:
            logger.info("Error during edit:", e)

