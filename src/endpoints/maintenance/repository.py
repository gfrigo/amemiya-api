from base64 import b64encode

from src.core.config import logger
from src.endpoints import generic_repository
from .queries import AssembleStatement


class MaintenanceRepository:

    @staticmethod
    def fetch(cursor, query_filter: dict) -> dict | list | None:
        logger.info("FETCH MAINTENANCE REPOSITORY HIT")

        try:
            select_stmt = AssembleStatement.get_maintenance_data(query_filter)
            logger.info(f"To execute: {select_stmt}")

            cursor.execute(select_stmt)
            logger.info("Executed")

            result = cursor.fetchall()

            if not result:
                return None

            data: list = []
            for entry in result:
                (
                    maintenance_id,
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
                    maintenance_type,
                    maintenance_origin,
                    maintenance_responsible,
                    cost,
                    maintenance_date
                ) = entry

                encoded_file_data = b64encode(file_data).decode("utf-8")

                data.append({
                    "maintenance_id": maintenance_id,
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
                    "maintenance_type": maintenance_type,
                    "maintenance_origin": maintenance_origin,
                    "maintenance_responsible": maintenance_responsible,
                    "cost": float(cost),
                    "maintenance_date": str(maintenance_date)
                })

            return data

        except IndexError:
            return None


    @staticmethod
    def add(cursor, data: dict):
        logger.info("ADD MAINTENANCE REPOSITORY HIT")

        try:
            insert_stmt = AssembleStatement.add_maintenance(data)
            logger.info(f"To execute: {insert_stmt}")

            cursor.execute(insert_stmt)
            logger.info("Executed")

        except Exception as e:
            print(e)
            return None

        return cursor.lastrowid

    @staticmethod
    def edit(cursor, data: dict):
        logger.info("EDIT MAINTENANCE REPOSITORY HIT")

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
        logger.info("REMOVE MAINTENANCE REPOSITORY HIT")

        try:
            remove_stmt = generic_repository.remove(data)
            logger.info(f"To execute: {remove_stmt}")

            cursor.execute(remove_stmt)
            logger.info("Executed")

        except Exception as e:
            logger.info("Error during edit:", e)
