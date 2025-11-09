from src.core.logging_config import logger
from src.core.database import start_connection, start_cursor
from .repository import GeopointRepository
from src.core.config import settings
from src.core.utils import get_geocode_data


def fetch_geopoint_service(request_data: dict) -> dict:
    logger.info("FETCH GEOPOINT SERVICE HIT")

    request_data = {k: v for k, v in request_data.items() if v is not None}

    query_filter = {
        "company_id": {"type": "index",
                     "value": request_data.get("company_id"),
                     "table": "Geopoints"}
    }

    with start_connection(settings.DB_HOST, settings.DB_USER, settings.DB_PASSWORD, settings.DB_SCHEMA) as conn:
        with start_cursor(conn) as cursor:

            geopoints: dict = GeopointRepository.fetch(cursor, query_filter)

    return geopoints

def add_geopoint_service(request_data: dict):
    logger.info("ADD GEOPOINT SERVICE HIT")

    request_data = {k: v for k, v in request_data.items() if v is not None}

    latitude, longitude = request_data.get("latitude"), request_data.get("longitude")

    geocode_data = get_geocode_data(latitude, longitude)

    country = geocode_data['country']
    state = geocode_data['state'] if geocode_data['state'] else None
    if geocode_data.get("county"):
        city = geocode_data['county']
        district = geocode_data['city']
    else:
        city = geocode_data['city']
        district = None

    request_data["country"] = country
    request_data["state"] = state
    request_data["city"] = city
    request_data["district"] = district

    with start_connection(settings.DB_HOST, settings.DB_USER, settings.DB_PASSWORD, settings.DB_SCHEMA) as conn:
        with start_cursor(conn) as cursor:

            geopoint_id: int = GeopointRepository.add(cursor, request_data)

        conn.commit()
        logger.info("Changes committed")

    if geopoint_id:
        return geopoint_id

    else:
        return None

def edit_geopoint_service(request_data: dict):
    logger.info("EDIT GEOPOINT SERVICE HIT")

    request_data = {k: v for k, v in request_data.items() if v is not None}

    request_geopoint_id: int = request_data.get("geopoint_id")

    request_latitude: float = request_data.get("latitude")
    request_longitude: float = request_data.get("longitude")

    if request_latitude and request_longitude:
        geocode_data = get_geocode_data(request_latitude, request_longitude)

        country = geocode_data['country']
        state = geocode_data['state'] if geocode_data['state'] else None
        if geocode_data.get("county"):
            city = geocode_data['county']
            district = geocode_data['city']
        else:
            city = geocode_data['city']
            district = None

        request_data["country"] = country
        request_data["state"] = state
        request_data["city"] = city
        request_data["district"] = district

    query_filter = {
        "geopoint_id": {"type": "index",
                        "value": request_geopoint_id,
                        "table": "Geopoints"}
    }

    query_data = {
        "table": "Geopoints",
        "filter": query_filter,
        "data": request_data
    }

    with start_connection(settings.DB_HOST, settings.DB_USER, settings.DB_PASSWORD, settings.DB_SCHEMA) as conn:
        with start_cursor(conn) as cursor:

            geopoint_data: dict = GeopointRepository.fetch(cursor, query_filter)

            if not geopoint_data:
                raise IndexError("Geopoint ID has no data")

            GeopointRepository.edit(cursor, query_data)

        conn.commit()

def remove_geopoint_service(geopoint_id: int):
    logger.info("REMOVE GEOPOINT SERVICE HIT")

    query_filter = {
        "geopoint_id": {"type": "index",
                        "value": geopoint_id,
                        "table": "Geopoints"}
    }

    query_data = {
        "table": "Geopoints",
        "filter": query_filter
    }

    with start_connection(settings.DB_HOST, settings.DB_USER, settings.DB_PASSWORD, settings.DB_SCHEMA) as conn:
        with start_cursor(conn) as cursor:
            geopoint_data: dict = GeopointRepository.fetch(cursor, query_filter)

            if not geopoint_data:
                raise IndexError("Geopoint ID has no data")

            GeopointRepository.remove(cursor, query_data)

        conn.commit()
