from src.core.logging_config import logger
from src.core.database import start_connection, start_cursor
from .repository import DeliveryRepository
from .model import DeliveryDataRequest
from src.endpoints import generic_repository
from src.core.config import settings
from secrets import token_hex
from src.core.utils import get_geocode_data
from src.endpoints.geopoint.repository import GeopointRepository


def fetch_delivery_service(request_data: dict) -> list:
    logger.info("FETCH DELIVERY SERVICE HIT")

    request_data = {k: v for k, v in request_data.items() if v is not None}

    query_filter = {
        "company_id": {"type": "index",
                        "value": request_data.get("company_id"),
                        "table": "Deliveries"},
        "user_id": {"type": "index",
                    "value": request_data.get("user_id"),
                    "table": "Deliveries"},
        "vehicle_id": {"type": "index",
                       "value": request_data.get("vehicle_id"),
                       "table": "Deliveries"},
        "delivery_code": {"type": "similarity",
                          "value": request_data.get("delivery_code"),
                          "table": "Deliveries"},
        "payload_item": {"type": "similarity",
                         "value": request_data.get("payload_item"),
                         "table": "Deliveries"},
        "payload_quantity": {"type": "value_range",
                             "value": (
                                 request_data.get("payload_quantity_range_lower"),
                                 request_data.get("payload_quantity_range_higher")
                             ),
                             "table": "Deliveries"},
        "payload_quantity_unit": {"type": "index",
                                  "value": request_data.get("payload_quantity_unit"),
                                  "table": "Deliveries"},
        "payload_weight": {"type": "value_range",
                             "value": (
                                 request_data.get("payload_weight_range_lower"),
                                 request_data.get("payload_weight_range_higher")
                             ),
                             "table": "Deliveries"},
        "estimated_delivery_time": {"type": "date_range",
                        "value": (
                            request_data.get("estimated_delivery_time_date_range_start"),
                            request_data.get("estimated_delivery_time_date_range_end")
                        ),
                        "table": "Deliveries"},
        "start_time_date": {"type": "date_range",
                                    "value": (
                                        request_data.get("start_time_date_range_start"),
                                        request_data.get("start_time_date_range_end")
                                    ),
                                    "table": "Deliveries"},
        "start_label": {"type": "similarity",
                        "value": request_data.get("start_label"),
                        "table": "Deliveries"},
        "start_city": {"type": "similarity",
                       "value": request_data.get("start_city"),
                       "table": "Deliveries"},
        "start_district": {"type": "similarity",
                           "value": request_data.get("start_district"),
                           "table": "Deliveries"},
        "finish_time_date": {"type": "date_range",
                             "value": (
                                 request_data.get("finish_time_date_range_start"),
                                 request_data.get("finish_time_date_range_end")
                             ),
                             "table": "Deliveries"},
        "end_label": {"type": "similarity",
                      "value": request_data.get("end_label"),
                      "table": "Deliveries"},
        "end_city": {"type": "similarity",
                     "value": request_data.get("end_city"),
                     "table": "Deliveries"},
        "end_district": {"type": "similarity",
                         "value": request_data.get("end_district"),
                         "table": "Deliveries"},
        "delivery_status": {"type": "index",
                            "value": request_data.get("delivery_status"),
                            "table": "Deliveries"}
    }

    with start_connection(settings.DB_HOST, settings.DB_USER, settings.DB_PASSWORD, settings.DB_SCHEMA) as conn:
        with start_cursor(conn) as cursor:

            result: list = DeliveryRepository.fetch(cursor, query_filter)

    return result

def add_delivery_service(request_data: dict):
    logger.info("ADD DELIVERY SERVICE HIT")

    request_data = {k: v for k, v in request_data.items() if v is not None}

    request_company_id: int = request_data.get("company_id")

    request_start_geopoint_id: int | None = request_data.pop("start_geopoint_id", None)
    if not request_start_geopoint_id:
        request_start_latitude: float | None = request_data.get("start_latitude")
        request_start_longitude: float | None = request_data.get("start_longitude")
        if not request_start_latitude or not request_start_longitude:
            raise ValueError("Start geopoint_id or latitude and longitude are required")

    request_end_geopoint_id: int | None = request_data.pop("end_geopoint_id", None)
    if not request_end_geopoint_id:
        request_end_latitude: float | None = request_data.get("end_latitude")
        request_end_longitude: float | None = request_data.get("end_longitude")
        if not request_end_latitude or not request_end_longitude:
            raise ValueError("End geopoint_id or latitude and longitude are required")

    query_filter = {
        "company_id": {"type": "index",
                       "value": request_company_id,
                       "table": "Companies"}
    }

    with start_connection(settings.DB_HOST, settings.DB_USER, settings.DB_PASSWORD, settings.DB_SCHEMA) as conn:
        with start_cursor(conn) as cursor:
            company_code: str = generic_repository.fetch(cursor, "Companies", "company_code", query_filter)[0][0]
            if not company_code:
                raise IndexError("Company ID has no data")

            for _ in range(20):
                hex_code = token_hex(5)

                delivery_code: str = f"{company_code}-{hex_code}"

                request_data["delivery_code"] = delivery_code

                query_filter["delivery_code"] = {"type": "index",
                                                 "value": delivery_code,
                                                 "table": "Deliveries"}

                duplicate_data: dict = DeliveryRepository.fetch(cursor, query_filter)

                if not duplicate_data:
                    break

            else:
                raise RuntimeError("Failed to generate unique delivery code after multiple attempts")

            if request_start_geopoint_id:
                start_geopoint_query_filter = {
                    "geopoint_id": {"type": "index",
                                   "value": request_start_geopoint_id,
                                   "table": "Geopoints"}
                }

                start_geopoint_data: dict = GeopointRepository.fetch(cursor, start_geopoint_query_filter)
                start_label: str | None = start_geopoint_data["label"]
                start_latitude: float = start_geopoint_data["latitude"]
                start_longitude: float = start_geopoint_data["longitude"]
                start_city: str = start_geopoint_data["city"]
                start_district: str | None = start_geopoint_data["district"]

            else:
                try:
                    start_label = None
                    start_latitude = request_start_latitude
                    start_longitude = request_start_longitude
                    start_geocode_search = get_geocode_data(start_latitude, start_longitude)
                    if start_geocode_search.get("county"):
                        start_city = start_geocode_search['county']
                        start_district = start_geocode_search['city']
                    else:
                        start_city = start_geocode_search['city']
                        start_district = None
                except:
                    raise ValueError("Start latitude and longitude are required")

            if request_end_geopoint_id:
                end_geopoint_query_filter = {
                    "geopoint_id": {"type": "index",
                                   "value": request_end_geopoint_id,
                                   "table": "Geopoints"}
                }

                end_geopoint_data: dict = GeopointRepository.fetch(cursor, end_geopoint_query_filter)
                end_label: str | None = end_geopoint_data["label"]
                end_latitude: float = end_geopoint_data["latitude"]
                end_longitude: float = end_geopoint_data["longitude"]
                end_city: str = end_geopoint_data["city"]
                end_district: str | None = end_geopoint_data["district"]

            else:
                try:
                    end_label = None
                    end_latitude = request_end_latitude
                    end_longitude = request_end_longitude
                    end_geocode_search = get_geocode_data(end_latitude, end_longitude)
                    if end_geocode_search.get("county"):
                        end_city = end_geocode_search['county']
                        end_district = end_geocode_search['city']
                    else:
                        end_city = end_geocode_search['city']
                        end_district = None
                except:
                    raise ValueError("End latitude and longitude are required")

            request_data["start_label"] = start_label
            request_data["start_latitude"] = start_latitude
            request_data["start_longitude"] = start_longitude
            request_data["start_city"] = start_city
            request_data["start_district"] = start_district

            request_data["end_label"] = end_label
            request_data["end_latitude"] = end_latitude
            request_data["end_longitude"] = end_longitude
            request_data["end_city"] = end_city
            request_data["end_district"] = end_district

            print(request_data)

            delivery_id = DeliveryRepository.add(cursor, request_data)

        conn.commit()

    return delivery_id

def edit_delivery_service(request_data: dict):
    logger.info("EDIT DELIVERY SERVICE HIT")

    request_data = {k: v for k, v in request_data.items() if v is not None and k != "attachment_id"}

    request_delivery_id: int = request_data.get("delivery_id")

    query_filter = {
        "delivery_id": {"type": "index",
                        "value": request_delivery_id,
                        "table": "Deliveries"}
    }

    query_data = {
        "table": "Deliveries",
        "filter": query_filter,
        "data": request_data
    }

    with start_connection(settings.DB_HOST, settings.DB_USER, settings.DB_PASSWORD, settings.DB_SCHEMA) as conn:
        with start_cursor(conn) as cursor:
            delivery_data: dict = DeliveryRepository.fetch(cursor, query_filter)

            if not delivery_data:
                raise IndexError("Delivery ID has no data")

            DeliveryRepository.edit(cursor, query_data)

        conn.commit()

def remove_delivery_service(delivery_id: int):
    logger.info("REMOVE DELIVERY SERVICE HIT")

    query_filter = {
        "delivery_id": {"type": "index",
                        "value": delivery_id,
                        "table": "Deliveries"}
    }

    query_data = {
        "table": "Deliveries",
        "filter": query_filter
    }

    with start_connection(settings.DB_HOST, settings.DB_USER, settings.DB_PASSWORD, settings.DB_SCHEMA) as conn:
        with start_cursor(conn) as cursor:
            delivery_data: dict = DeliveryRepository.fetch(cursor, query_filter)

            if not delivery_data:
                raise IndexError("Delivery ID has no data")

            DeliveryRepository.remove(cursor, query_data)

        conn.commit()
