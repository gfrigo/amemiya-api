from src.core.config import logger
from src.endpoints import generic_repository
from .queries import AssembleStatement


class VehicleRepository:

    @staticmethod
    def fetch(cursor, query_filter: dict) -> dict | list | None:
        logger.info("FETCH VEHICLE REPOSITORY HIT")

        try:

            select_stmt = AssembleStatement.get_vehicle_data(query_filter)
            logger.info(f"To execute: {select_stmt}")

            cursor.execute(select_stmt)
            logger.info("Executed")

            result = cursor.fetchall()

            vehicles_data: list = []

            vehicles = result
            for vehicle_entry in vehicles:
                vehicle_id, vehicle_name, license_plate, brand, model, year, notes, company_id, company_name, last_user_id, user_name, last_used, active_vehicle = vehicle_entry

                vehicles_data.append({
                    "vehicle_id": vehicle_id,
                    "vehicle_name": vehicle_name,
                    "license_plate": license_plate,
                    "brand": brand,
                    "model": model,
                    "year": year,
                    "notes": notes,
                    "company_id": company_id,
                    "company_name": company_name,
                    "last_user_id": last_user_id,
                    "last_user_name": user_name,
                    "last_used": None if last_used is None else str(last_used),
                    "active_vehicle": active_vehicle == 1
                })

            return vehicles_data

        except IndexError:
            return None

        except ValueError:
            return None

    @staticmethod
    def add(cursor, data: dict):
        logger.info("ADD VEHICLE REPOSITORY HIT")

        try:
            insert_stmt = AssembleStatement.add_vehicle(tuple(data.keys()), tuple(data.values()))
            logger.info(f"To execute: {insert_stmt}")

            cursor.execute(insert_stmt)
            logger.info("Executed")

        except Exception as e:
            print(e)
            return None

        return cursor.lastrowid

    @staticmethod
    def edit(cursor, data: dict):
        logger.info("EDIT VEHICLE REPOSITORY HIT")

        try:
            update_stmt = generic_repository.edit(data)
            logger.info(f"To execute: {update_stmt}")

            cursor.execute(update_stmt)
            logger.info("Executed")

        except Exception as e:
            logger.info("Error during edit:", e)

    @staticmethod
    def remove(cursor, data: dict):
        logger.info("REMOVE VEHICLE REPOSITORY HIT")

        try:
            remove_stmt = generic_repository.remove(data)
            logger.info(f"To execute: {remove_stmt}")

            cursor.execute(remove_stmt)
            logger.info("Executed")

        except Exception as e:
            logger.info("Error during remotion:", e)

