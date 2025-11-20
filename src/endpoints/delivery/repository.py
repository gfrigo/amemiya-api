from src.core.config import logger
from src.endpoints import generic_repository
from .queries import AssembleStatement


class DeliveryRepository:

    @staticmethod
    def fetch(cursor, query_filter: dict) -> dict | list | None:
        logger.info("FETCH DELIVERY REPOSITORY HIT")

        try:
            select_stmt = AssembleStatement.get_delivery_data(query_filter)
            logger.info(f"To execute: {select_stmt}")

            cursor.execute(select_stmt)
            logger.info("Executed")

            result = cursor.fetchall()

            if not result:
                return None

            data: list = []
            for entry in result:
                (
                    delivery_id,
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
                    delivery_code,
                    payload_item,
                    payload_quantity,
                    payload_quantity_unit,
                    payload_weight,
                    estimated_delivery_time,
                    start_time,
                    start_label,
                    start_latitude,
                    start_longitude,
                    start_city,
                    start_district,
                    finish_time,
                    end_label,
                    end_latitude,
                    end_longitude,
                    end_city,
                    end_district,
                    delivery_status
                ) = entry

                data.append({
                    "delivery_id": delivery_id,
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
                    "delivery_code": delivery_code,
                    "payload_item": payload_item,
                    "payload_quantity": float(payload_quantity),
                    "payload_quantity_unit": payload_quantity_unit,
                    "payload_weight": float(payload_weight),
                    "estimated_delivery_time": None if estimated_delivery_time is None else str(estimated_delivery_time),
                    "start_time": None if start_time is None else str(start_time),
                    "start_label": start_label,
                    "start_latitude": float(start_latitude),
                    "start_longitude": float(start_longitude),
                    "start_city": start_city,
                    "start_district": start_district,
                    "finish_time": None if finish_time is None else str(finish_time),
                    "end_label": end_label,
                    "end_latitude": float(end_latitude),
                    "end_longitude": float(end_longitude),
                    "end_city": end_city,
                    "end_district": end_district,
                    "delivery_status": delivery_status
                })

            return data

        except IndexError:
            return None


    @staticmethod
    def add(cursor, data: dict):
        logger.info("ADD DELIVERY REPOSITORY HIT")

        try:

            insert_stmt = AssembleStatement.add_delivery(data)
            logger.info(f"To execute: {insert_stmt}")

            cursor.execute(insert_stmt)
            logger.info("Executed")

        except Exception as e:
            print(e)
            return None

        return cursor.lastrowid

    @staticmethod
    def edit(cursor, data: dict):
        logger.info("EDIT DELIVERY REPOSITORY HIT")

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
        logger.info("REMOVE DELIVERY REPOSITORY HIT")

        try:
            remove_stmt = generic_repository.remove(data)
            logger.info(f"To execute: {remove_stmt}")

            cursor.execute(remove_stmt)
            logger.info("Executed")

        except Exception as e:
            logger.info("Error during edit:", e)


