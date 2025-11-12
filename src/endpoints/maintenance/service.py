from src.core.config import logger
from src.core.config import settings
from src.core.database import start_connection, start_cursor
from .repository import MaintenanceRepository


def fetch_maintenance_service(request_data: dict) -> list:
    logger.info("FETCH MAINTENANCE SERVICE HIT")

    request_data = {k: v for k, v in request_data.items() if v is not None}

    query_filter = {
        "company_id": {"type": "index",
                       "value": request_data.get("company_id"),
                       "table": "Maintenances"},
        "user_id": {"type": "index",
                    "value": request_data.get("user_id"),
                    "table": "Maintenances"},
        "vehicle_id": {"type": "index",
                    "value": request_data.get("vehicle_id"),
                    "table": "Maintenances"},
        "cost": {"type": "value_range",
                 "value": (request_data.get("cost_range_lower"), request_data.get("cost_range_higher")),
                 "table": "Maintenances"},
        "maintenance_type": {"type": "similarity",
                             "value": request_data.get("maintenance_type"),
                             "table": "Maintenances"},
        "maintenance_origin": {"type": "similarity",
                               "value": request_data.get("maintenance_origin"),
                               "table": "Maintenances"},
        "maintenance_responsible": {"type": "similarity",
                                    "value": request_data.get("maintenance_responsible"),
                                    "table": "Maintenances"},
        "maintenance_date": {"type": "date_range",
                             "value": (request_data.get("maintenance_date_range_start"), request_data.get("maintenance_date_range_end")),
                             "table": "Maintenances"}
    }

    with start_connection(settings.db_credentials) as conn:
        with start_cursor(conn) as cursor:

            maintenances: list = MaintenanceRepository.fetch(cursor, query_filter)

    return maintenances

def add_maintenance_service(request_data: dict):
    logger.info("ADD MAINTENANCE SERVICE HIT")

    request_data = {k: v for k, v in request_data.items() if v is not None}

    with start_connection(settings.db_credentials) as conn:
        with start_cursor(conn) as cursor:

            maintenance_id: int = MaintenanceRepository.add(cursor, request_data)

        conn.commit()
        logger.info("Changes committed")

    if maintenance_id:
        return maintenance_id

    else:
        return None

def edit_maintenance_service(request_data: dict):
    logger.info("EDIT MAINTENANCE SERVICE HIT")

    request_data = {k: v for k, v in request_data.items() if v is not None and k != "attachment_id"}

    request_maintenance_id: int = request_data.get("maintenance_id")

    query_filter = {
        "maintenance_id": {"type": "index",
                       "value": request_maintenance_id,
                       "table": "Maintenances"}
    }

    query_data = {
        "table": "Maintenances",
        "filter": query_filter,
        "data": request_data
    }

    with start_connection(settings.db_credentials) as conn:
        with start_cursor(conn) as cursor:

            maintenance_data: dict = MaintenanceRepository.fetch(cursor, query_filter)

            if not maintenance_data:
                raise IndexError("Maintenance ID has no data")

            MaintenanceRepository.edit(cursor, query_data)

        conn.commit()

def remove_maintenance_service(maintenance_id: int):
    logger.info("REMOVE MAINTENANCE SERVICE HIT")

    query_filter = {
        "maintenance_id": {"type": "index",
                        "value": maintenance_id,
                        "table": "Maintenances"}
    }

    query_data = {
        "table": "Maintenances",
        "filter": query_filter
    }

    with start_connection(settings.db_credentials) as conn:
        with start_cursor(conn) as cursor:
            maintenance_data: dict = MaintenanceRepository.fetch(cursor, query_filter)

            if not maintenance_data:
                raise IndexError("Maintenance ID has no data")

            MaintenanceRepository.remove(cursor, query_data)

        conn.commit()
