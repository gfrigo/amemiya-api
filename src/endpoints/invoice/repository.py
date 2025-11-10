from .queries import AssembleStatement
from src.core.logging_config import logger
from src.endpoints.generic_repository import get_last_entry
from src.register import Register
from base64 import b64encode
from src.endpoints import generic_repository


class InvoiceRepository:

    @staticmethod
    def fetch(cursor, query_filter: dict) -> dict | list | None:
        logger.info("FETCH INVOICE REPOSITORY HIT")

        try:
            select_stmt = AssembleStatement.get_invoice_data(query_filter)
            logger.info(f"To execute: {select_stmt}")

            cursor.execute(select_stmt)
            logger.info("Executed")

            result = cursor.fetchall()

            if not result:
                return None

            data: list = []
            for entry in result:
                (
                    invoice_id,
                    company_id,
                    company_name,
                    user_id,
                    user_name,
                    attachment_id,
                    file_data,
                    file_type,
                    upload_date,
                    cost,
                    purchase_type,
                    invoice_origin,
                    invoice_number,
                    invoice_series,
                    emission_date
                ) = entry

                encoded_file_data = b64encode(file_data).decode("utf-8")

                data.append({
                    "invoice_id": invoice_id,
                    "company_id": company_id,
                    "company_name": company_name,
                    "user_id": user_id,
                    "user_name": user_name,
                    "attachment_id": attachment_id,
                    "file_data": encoded_file_data,
                    "file_type": file_type,
                    "upload_date": str(upload_date),
                    "cost": float(cost),
                    "purchase_type": purchase_type,
                    "invoice_origin": invoice_origin,
                    "invoice_number": invoice_number,
                    "invoice_series": invoice_series,
                    "emission_date": str(emission_date)
                })

            return data

        except IndexError:
            return None


    @staticmethod
    def add(cursor, data: dict):
        logger.info("ADD INVOICE REPOSITORY HIT")

        try:
            insert_stmt = AssembleStatement.add_invoice(data)
            logger.info(f"To execute: {insert_stmt}")

            cursor.execute(insert_stmt)
            logger.info("Executed")

        except Exception as e:
            print(e)
            return None

        return cursor.lastrowid

    @staticmethod
    def edit(cursor, data: dict):
        logger.info("EDIT GEOPOINT REPOSITORY HIT")

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
        logger.info("REMOVE GEOPOINT REPOSITORY HIT")

        try:
            remove_stmt = generic_repository.remove(data)
            logger.info(f"To execute: {remove_stmt}")

            cursor.execute(remove_stmt)
            logger.info("Executed")

        except Exception as e:
            logger.info("Error during edit:", e)


