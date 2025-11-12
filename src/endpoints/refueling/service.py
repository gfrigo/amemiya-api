from src.core.config import settings
from src.core.database import start_connection, start_cursor
from src.core.config import logger
from .repository import RefuelingRepository


def fetch_refueling_service(request_data: dict) -> list:
    logger.info("FETCH REFUELING SERVICE HIT")

    request_data = {k: v for k, v in request_data.items() if v is not None}

    query_filter = {
        "company_id": {"type": "index",
                       "value": request_data.get("company_id"),
                       "table": "Refuelings"},
        "user_id": {"type": "index",
                    "value": request_data.get("user_id"),
                    "table": "Refuelings"},
        "vehicle_id": {"type": "index",
                    "value": request_data.get("vehicle_id"),
                    "table": "Refuelings"},
        "refueling_type": {"type": "similarity",
                           "value": request_data.get("refueling_type"),
                           "table": "Refuelings"},
        "refueling_origin": {"type": "similarity",
                             "value": request_data.get("refueling_origin"),
                             "table": "Refuelings"},
        "refueling_station": {"type": "similarity",
                              "value": request_data.get("refueling_station"),
                              "table": "Refuelings"},
        "current_kilometrage": {"type": "value_range",
                                "value": (request_data.get("kilometrage_range_lower"), request_data.get("kilometrage_range_higher")),
                                "table": "Refuelings"},
        "refueling_volume": {"type": "value_range",
                             "value": (request_data.get("volume_range_lower"), request_data.get("volume_range_higher")),
                             "table": "Refuelings"},
        "cost": {"type": "value_range",
                 "value": (request_data.get("cost_range_lower"), request_data.get("cost_range_higher")),
                 "table": "Refuelings"},
        "refueling_date": {"type": "date_range",
                           "value": (request_data.get("refueling_date_range_start"), request_data.get("refueling_date_range_end")),
                           "table": "Refuelings"}
    }

    with start_connection(settings.db_credentials) as conn:
        with start_cursor(conn) as cursor:

            refuelings: list = RefuelingRepository.fetch(cursor, query_filter)

    return refuelings

def add_refueling_service(request_data: dict):
    logger.info("ADD REFUELING SERVICE HIT")

    request_data = {k: v for k, v in request_data.items() if v is not None}

    with start_connection(settings.db_credentials) as conn:
        with start_cursor(conn) as cursor:

            refueling_id: int = RefuelingRepository.add(cursor, request_data)

        conn.commit()
        logger.info("Changes committed")

    if refueling_id:
        return refueling_id

    else:
        return None

def edit_refueling_service(request_data: dict):
    logger.info("EDIT REFUELING SERVICE HIT")

    request_data = {k: v for k, v in request_data.items() if v is not None and k != "attachment_id"}

    request_refueling_id: int = request_data.get("refueling_id")

    query_filter = {
        "refueling_id": {"type": "index",
                       "value": request_refueling_id,
                       "table": "Refuelings"}
    }

    query_data = {
        "table": "Refuelings",
        "filter": query_filter,
        "data": request_data
    }

    with start_connection(settings.db_credentials) as conn:
        with start_cursor(conn) as cursor:

            refueling_data: dict = RefuelingRepository.fetch(cursor, query_filter)

            if not refueling_data:
                raise IndexError("Refueling ID has no data")

            RefuelingRepository.edit(cursor, query_data)

        conn.commit()

def remove_refueling_service(refueling_id: int):
    logger.info("REMOVE REFUELING SERVICE HIT")

    query_filter = {
        "refueling_id": {"type": "index",
                        "value": refueling_id,
                        "table": "Refuelings"}
    }

    query_data = {
        "table": "Refuelings",
        "filter": query_filter
    }

    with start_connection(settings.db_credentials) as conn:
        with start_cursor(conn) as cursor:
            refueling_data: dict = RefuelingRepository.fetch(cursor, query_filter)

            if not refueling_data:
                raise IndexError("Refueling ID has no data")

            RefuelingRepository.remove(cursor, query_data)

        conn.commit()
