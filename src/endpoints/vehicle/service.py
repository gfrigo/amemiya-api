from src.core.logging_config import logger
from src.core.database import start_connection, start_cursor
from .repository import VehicleRepository
from .schema import VehicleDataRequest
from src.core.utils import check_missing_fields
from src.core.config import settings


def fetch_vehicle_service(request: VehicleDataRequest) -> dict | None:
    logger.info("FETCH VEHICLE SERVICE HIT")
    data = request.model_dump()
    required_fields = ["company_id"]
    check_missing_fields(data, required_fields)

    with start_connection(settings.DB_HOST, settings.DB_USER, settings.DB_PASSWORD, settings.DB_SCHEMA) as conn:
        with start_cursor(conn) as cursor:
            result: list = VehicleRepository.fetch(cursor, data, None)

            logger.info(f"Query result: {result}")

            vehicle_data = {}
            for vehicle_entry in result:
                vehicle_data[vehicle_entry[0]] = {
                    "company_id": vehicle_entry[1],
                    "name": vehicle_entry[2],
                    "license_plate": vehicle_entry[3],
                    "brand": vehicle_entry[4],
                    "model": vehicle_entry[5],
                    "year": vehicle_entry[6],
                    "notes": vehicle_entry[7],
                    "last_used": vehicle_entry[8],
                    "last_user_id": vehicle_entry[9],
                    "active": True if vehicle_entry[10] == 1 else False
                }

            return vehicle_data

def add_vehicle_service(request: VehicleDataRequest):
    logger.info("ADD VEHICLE SERVICE HIT")
    data = request.model_dump()
    required_fields = [
        "company_id",
        "name",
        "license_plate",
        "brand",
        "model",
        "year"
    ]
    check_missing_fields(data, required_fields)

    with start_connection(settings.DB_HOST, settings.DB_USER, settings.DB_PASSWORD, settings.DB_SCHEMA) as conn:
        with start_cursor(conn) as cursor:
            VehicleRepository.add(cursor, data)
            conn.commit()
    return "Vehicle added successfully"

def edit_vehicle_service(request: VehicleDataRequest):
    logger.info("EDIT VEHICLE SERVICE HIT")
    data = request.model_dump()
    required_fields = ["vehicle_id"]
    check_missing_fields(data, required_fields)

    with start_connection(settings.DB_HOST, settings.DB_USER, settings.DB_PASSWORD, settings.DB_SCHEMA) as conn:
        with start_cursor(conn) as cursor:
            vehicle_data: list = VehicleRepository.fetch(cursor, data, None)
            if not vehicle_data:
                return "vehicle_id has no data"

            logger.info(f"Query result: {vehicle_data}")

            VehicleRepository.edit(cursor, data)
            conn.commit()
    return "Vehicle edited successfully"

def remove_vehicle_service(request: VehicleDataRequest):
    logger.info("REMOVE VEHICLE SERVICE HIT")
    data = request.model_dump()
    required_fields = ["vehicle_id"]
    check_missing_fields(data, required_fields)

    with start_connection(settings.DB_HOST, settings.DB_USER, settings.DB_PASSWORD, settings.DB_SCHEMA) as conn:
        with start_cursor(conn) as cursor:
            vehicle_data: dict = VehicleRepository.fetch(cursor, data)
            if not vehicle_data:
                return "vehicle_id has no data"

            VehicleRepository.remove(cursor, data)
            conn.commit()
    return "Vehicle removed successfully"