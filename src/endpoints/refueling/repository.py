from .queries import AssembleStatement
from src.core.logging_config import logger
from src.endpoints.generic_repository import get_last_entry
from src.register import Register
from base64 import b64encode
from src.endpoints import generic_repository


class RefuelingRepository:

    @staticmethod
    def fetch(cursor, query_filter: dict) -> dict | list | None:
        logger.info("FETCH REFUELING REPOSITORY HIT")

        try:
            select_stmt = AssembleStatement.get_refueling_data(query_filter)
            logger.info(f"To execute: {select_stmt}")

            cursor.execute(select_stmt)
            logger.info("Executed")

            result = cursor.fetchall()

            if not result:
                return None

            data: list = []
            for entry in result:
                (
                    refueling_id,
                    company_id,
                    company_name,
                    user_id,
                    user_name,
                    vehicle_id,
                    vehicle_name,
                    license_plate,
                    brand,
                    model,
                    year,
                    attachment_id,
                    file_data,
                    file_type,
                    upload_date,
                    refueling_type,
                    refueling_origin,
                    refueling_station,
                    current_kilometrage,
                    refueling_volume,
                    cost,
                    refueling_date
                ) = entry

                encoded_file_data = b64encode(file_data).decode("utf-8")

                data.append({
                    "refueling_id": refueling_id,
                    "company_id": company_id,
                    "company_name": company_name,
                    "user_id": user_id,
                    "user_name": user_name,
                    "vehicle_id": vehicle_id,
                    "vehicle_name": vehicle_name,
                    "license_plate": license_plate,
                    "brand": brand,
                    "model": model,
                    "year": year,
                    "attachment_id": attachment_id,
                    "file_data": encoded_file_data,
                    "file_type": file_type,
                    "upload_date": str(upload_date),
                    "refueling_type": refueling_type,
                    "refueling_origin": refueling_origin,
                    "refueling_station": refueling_station,
                    "current_kilometrage": current_kilometrage,
                    "refueling_volume": refueling_volume,
                    "cost": float(cost),
                    "refueling_date": str(refueling_date)
                })

            return data

        except IndexError:
            return None


    @staticmethod
    def add(cursor, data: dict):
        logger.info("ADD REFUELING REPOSITORY HIT")

        try:
            insert_stmt = AssembleStatement.add_refueling(data)
            logger.info(f"To execute: {insert_stmt}")

            cursor.execute(insert_stmt)
            logger.info("Executed")

        except Exception as e:
            print(e)
            return None

        return cursor.lastrowid

    @staticmethod
    def edit(cursor, data: dict):
        logger.info("EDIT REFUELING REPOSITORY HIT")

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
        logger.info("REMOVE REFUELING REPOSITORY HIT")

        try:
            remove_stmt = generic_repository.remove(data)
            logger.info(f"To execute: {remove_stmt}")

            cursor.execute(remove_stmt)
            logger.info("Executed")

        except Exception as e:
            logger.info("Error during edit:", e)
