from .queries import AssembleStatement
from src.core.logging_config import logger
from src.register import Register
from base64 import b64encode


class AttachmentRepository:

    @staticmethod
    def fetch(cursor, query_filter: dict) -> dict | None:
        logger.info("FETCH ATTACHMENT REPOSITORY HIT")

        try:
            select_stmt = AssembleStatement.get_attachment_data(query_filter)
            logger.info(f"To execute: {select_stmt}")

            cursor.execute(select_stmt)
            logger.info("Executed")

            result = cursor.fetchall()

            if not result:
                return None

            data: dict = {}
            for entry in result:
                attachment_id, company_name, user_name, file_data, file_type, attachment_type, upload_date = entry

                encoded_file_data = b64encode(file_data).decode("utf-8")

                file_name = f"test_output.{file_type}"
                with open(file_name, "wb") as f:
                    f.write(file_data)

                data[attachment_id] = {
                    "company_name": company_name,
                    "user_name": user_name,
                    "file_data": encoded_file_data,
                    "file_type": file_type,
                    "attachment_type": attachment_type,
                    "upload_date": upload_date
                }

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

    @staticmethod
    def edit(cursor, attachment_id, data: dict):
        logger.info("EDIT ATTACHMENT REPOSITORY HIT")

        try:
            update_stmt = AssembleStatement.edit_attachment(attachment_id, data)
            logger.info(f"To execute: {update_stmt}")

            cursor.execute(update_stmt, tuple(v for v in data.values() if v is not None))
            logger.info("Executed")

        except Exception as e:
            print(e)
            return None

    @staticmethod
    def remove(cursor, attachment_id: int):
        logger.info("REMOVE USER REPOSITORY HIT")

        Register.remove(cursor, "user", f"user_id = {data['user_id']}")

