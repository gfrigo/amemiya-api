from src.core.logging_config import logger
from src.core.database import start_connection, start_cursor
from .repository import VehicleRepository
from .model import VehicleDataRequest
from src.core.utils import check_missing_fields
from src.core.config import settings


def fetch_vehicle_service(request_data: dict) -> dict | None:
    logger.info("FETCH VEHICLE SERVICE HIT")

    request_data = {k: v for k, v in request_data.items() if v is not None}

    query_filter = {
        "vehicle_id": {"type": "index",
                       "value": request_data.get("vehicle_id"),
                       "table": "Vehicles"},
        "company_id": {"type": "index",
                       "value": request_data.get("company_id"),
                       "table": "Vehicles"},
        "vehicle_name": {"type": "similarity",
                         "value": request_data.get("vehicle_name"),
                         "table": "Vehicles"},
        "license_plate": {"type": "similarity",
                          "value": request_data.get("license_plate"),
                          "table": "Vehicles"},
        "brand": {"type": "index",
                  "value": request_data.get("brand"),
                  "table": "Vehicles"},
        "model": {"type": "similarity",
                  "value": request_data.get("model"),
                  "table": "Vehicles"},
        "year": {"type": "index",
                 "value": request_data.get("year"),
                 "table": "Vehicles"},
        "last_used": {"type": "date_range",
                      "value": (request_data.get("date_range_start"), request_data.get("date_range_end")),
                      "table": "Vehicles"},
        "last_user_id": {"type": "index",
                         "value": request_data.get("last_user_id"),
                         "table": "Vehicles"},
        "active_vehicle": {"type": "index",
                           "value": request_data.get("active_vehicle"),
                           "table": "Vehicles"}
    }

    with start_connection(settings.DB_HOST, settings.DB_USER, settings.DB_PASSWORD, settings.DB_SCHEMA) as conn:
        with start_cursor(conn) as cursor:

            vehicles_data: dict = VehicleRepository.fetch(cursor, query_filter)

            return vehicles_data

def add_vehicle_service(request_data: dict):
    logger.info("ADD VEHICLE SERVICE HIT")

    request_data = {k: v for k, v in request_data.items() if v is not None}

    with start_connection(settings.DB_HOST, settings.DB_USER, settings.DB_PASSWORD, settings.DB_SCHEMA) as conn:
        with start_cursor(conn) as cursor:

            vehicle_id: int = VehicleRepository.add(cursor, request_data)

        conn.commit()

    if vehicle_id:
        return vehicle_id

    else:
        return None

def edit_vehicle_service(request_data: dict):
    logger.info("EDIT VEHICLE SERVICE HIT")

    request_data = {k: v for k, v in request_data.items() if v is not None}

    request_company_id: int = request_data.get("company_id")
    request_vehicle_id: int = request_data.get("vehicle_id")

    query_filter = {
        "company_id": {"type": "index",
                       "value": request_company_id,
                       "table": "Vehicles"},
        "vehicle_id": {"type": "index",
                    "value": request_vehicle_id,
                    "table": "Vehicles"}
    }

    query_data = {
        "table": "Vehicles",
        "filter": query_filter,
        "data": request_data
    }

    with start_connection(settings.DB_HOST, settings.DB_USER, settings.DB_PASSWORD, settings.DB_SCHEMA) as conn:
        with start_cursor(conn) as cursor:

            vehicle_data: dict = VehicleRepository.fetch(cursor, query_filter)

            if not vehicle_data:
                return "vehicle_id has no data"

            VehicleRepository.edit(cursor, query_data)

        conn.commit()

    return "Vehicle edited successfully"

def remove_vehicle_service(request_data: dict):
    logger.info("REMOVE VEHICLE SERVICE HIT")

    request_vehicle_id: int = request_data.get("vehicle_id")

    query_filter = {
        "vehicle_id": {"type": "index",
                       "value": request_vehicle_id,
                       "table": "Vehicles"}
    }

    query_data = {
        "table": "Vehicles",
        "filter": query_filter
    }

    with start_connection(settings.DB_HOST, settings.DB_USER, settings.DB_PASSWORD, settings.DB_SCHEMA) as conn:
        with start_cursor(conn) as cursor:

            vehicle_data: dict = VehicleRepository.fetch(cursor, query_filter)

            if not vehicle_data:
                return "vehicle_id has no data"

            VehicleRepository.remove(cursor, query_data)

        conn.commit()

    return "Vehicle removed successfully"