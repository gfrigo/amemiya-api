from src.core.config import logger
from src.core.config import settings
from src.core.database import start_connection, start_cursor
from .repository import InvoiceRepository


def fetch_invoice_service(request_data: dict) -> list:
    logger.info("FETCH INVOICE SERVICE HIT")

    request_data = {k: v for k, v in request_data.items() if v is not None}

    query_filter = {
        "company_id": {"type": "index",
                       "value": request_data.get("company_id"),
                       "table": "Invoices"},
        "user_id": {"type": "index",
                    "value": request_data.get("user_id"),
                    "table": "Invoices"},
        "cost": {"type": "value_range",
                 "value": (request_data.get("cost_range_lower"), request_data.get("cost_range_higher")),
                 "table": "Invoices"},
        "purchase_type": {"type": "index",
                          "value": request_data.get("purchase_type"),
                          "table": "Invoices"},
        "invoice_origin": {"type": "similarity",
                           "value": request_data.get("invoice_origin"),
                           "table": "Invoices"},
        "invoice_number": {"type": "similarity",
                           "value": request_data.get("contained_invoice_number"),
                           "table": "Invoices"},
        "invoice_series": {"type": "similarity",
                           "value": request_data.get("contained_invoice_series"),
                           "table": "Invoices"},
        "emission_date": {"type": "date_range",
                          "value": (request_data.get("emission_date_range_start"), request_data.get("emission_date_range_end")),
                          "table": "Invoices"}
    }

    with start_connection(settings.db_credentials) as conn:
        with start_cursor(conn) as cursor:

            invoices: list = InvoiceRepository.fetch(cursor, query_filter)

    return invoices

def add_invoice_service(request_data: dict):
    logger.info("ADD INVOICE SERVICE HIT")

    request_data = {k: v for k, v in request_data.items() if v is not None}

    request_invoice_number = request_data.get("invoice_number")
    request_invoice_series = request_data.get("invoice_series")

    if len(request_invoice_number) < 9:
        request_invoice_number = "0" * (9 - len(request_invoice_number)) + request_invoice_number
        request_data["invoice_number"] = request_invoice_number

    elif len(request_invoice_number) > 9:
        raise ValueError("Invoice number is too long")

    if not request_invoice_number.isnumeric():
        raise ValueError("Invoice number is not numeric")

    duplicate_query_filter = {
        "invoice_number": {"type": "index",
                           "value": request_invoice_number,
                           "table": "Invoices"},
        "invoice_series": {"type": "index",
                           "value": request_invoice_series,
                           "table": "Invoices"},
    }


    with start_connection(settings.db_credentials) as conn:
        with start_cursor(conn) as cursor:
            existing_invoice_data: dict = InvoiceRepository.fetch(cursor, duplicate_query_filter)

            if existing_invoice_data:
                raise ValueError(f"Invoice for {request_invoice_number}-{request_invoice_series} already exists")

            invoice_id: int = InvoiceRepository.add(cursor, request_data)

        conn.commit()
        logger.info("Changes committed")

    if invoice_id:
        return invoice_id

    else:
        return None

def edit_invoice_service(request_data: dict):
    logger.info("EDIT INVOICE SERVICE HIT")

    request_data = {k: v for k, v in request_data.items() if v is not None and k != "attachment_id"}

    request_invoice_number = request_data.get("invoice_number")

    if request_invoice_number:
        if len(request_invoice_number) < 9:
            request_invoice_number = "0" * (9 - len(request_invoice_number)) + request_invoice_number
            request_data["invoice_number"] = request_invoice_number

        elif len(request_invoice_number) > 9:
            raise ValueError("Invoice number is too long")

        if not request_invoice_number.isnumeric():
            raise ValueError("Invoice number is not numeric")

        request_data["invoice_number"] = request_invoice_number

    request_invoice_id: int = request_data.get("invoice_id")

    query_filter = {
        "invoice_id": {"type": "index",
                       "value": request_invoice_id,
                       "table": "Invoices"}
    }

    query_data = {
        "table": "Invoices",
        "filter": query_filter,
        "data": request_data
    }

    with start_connection(settings.db_credentials) as conn:
        with start_cursor(conn) as cursor:

            invoice_data: dict = InvoiceRepository.fetch(cursor, query_filter)

            if not invoice_data:
                raise IndexError("Invoice ID has no data")

            InvoiceRepository.edit(cursor, query_data)

        conn.commit()

def remove_invoice_service(invoice_id: int):
    logger.info("REMOVE INVOICE SERVICE HIT")

    query_filter = {
        "invoice_id": {"type": "index",
                        "value": invoice_id,
                        "table": "Invoices"}
    }

    query_data = {
        "table": "Invoices",
        "filter": query_filter
    }

    with start_connection(settings.db_credentials) as conn:
        with start_cursor(conn) as cursor:
            invoice_data: dict = InvoiceRepository.fetch(cursor, query_filter)

            if not invoice_data:
                raise IndexError("Invoice ID has no data")

            InvoiceRepository.remove(cursor, query_data)

        conn.commit()
