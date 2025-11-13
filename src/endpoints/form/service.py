from src.core.config import logger
from src.core.config import settings
from src.core.database import start_connection, start_cursor
from src.endpoints.user.repository import FormRepository


def fetch_form_service(request_data: dict) -> dict | list:
    logger.info("FETCH FORM SERVICE HIT")

    request_data = {k: v for k, v in request_data.items() if v is not None}

    print(request_data)

    query_filter = {
        "company_id": {"type": "index",
                       "value": request_data.get("company_id"),
                       "table": "Forms"},
        "user_id": {"type": "index",
                    "value": request_data.get("user_id"),
                    "table": "Forms"},
        "delivery_code": {"type": "similarity",
                          "value": request_data.get("delivery_code"),
                          "table": "Deliveries"},
        "was_delivered": {"type": "index",
                          "value": request_data.get("was_delivered"),
                          "table": "Forms"},
        "had_problem": {"type": "index",
                        "value": request_data.get("had_problem"),
                        "table": "Forms"},
        "who_received": {"type": "similarity",
                         "value": request_data.get("who_received"),
                         "table": "Forms"},
        "creation_datetime": {"type": "date_range",
                              "value": (request_data.get("creation_datetime_range_start"), request_data.get("creation_datetime_range_end")),
                              "table": "Forms"}
    }

    with start_connection(settings.db_credentials) as conn:
        with start_cursor(conn) as cursor:

            forms: list = FormRepository.fetch(cursor, query_filter)

    return forms

def add_form_service(request_data: dict):
    logger.info("ADD FORM SERVICE HIT")

    request_data = {k: v for k, v in request_data.items() if v is not None}

    with start_connection(settings.db_credentials) as conn:
        with start_cursor(conn) as cursor:

            form_id: int = FormRepository.add(cursor, request_data)

        conn.commit()

    if form_id:
        return form_id

    else:
        return None

def edit_form_service(request_data: dict):
    logger.info("EDIT FORM SERVICE HIT")

    request_data = {k: v for k, v in request_data.items() if v is not None}

    query_filter = {
        "form_id": {"type": "index",
                    "value": request_data.get("form_id"),
                    "table": "Forms"}
    }

    query_data = {
        "table": "Forms",
        "filter": query_filter,
        "data": request_data
    }

    with start_connection(settings.db_credentials) as conn:
        with start_cursor(conn) as cursor:

            form_data: dict = FormRepository.fetch(cursor, query_filter)

            if not form_data:
                raise IndexError("Form ID has no data")

            FormRepository.edit(cursor, query_data)

        conn.commit()

    return "Form edited successfully"

def remove_form_service(request_data: dict):
    logger.info("REMOVE FORM SERVICE HIT")

    query_filter = {
        "form_id": {"type": "index",
                    "value": request_data.get("form_id"),
                    "table": "Forms"}
    }

    query_data = {
        "table": "Forms",
        "filter": query_filter
    }

    with start_connection(settings.db_credentials) as conn:
        with start_cursor(conn) as cursor:

            form_data: dict = FormRepository.fetch(cursor, query_filter)

            if not form_data:
                raise IndexError("Form ID has no data")

            FormRepository.remove(cursor, query_data)

        conn.commit()
