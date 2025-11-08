from src.core.logging_config import logger
from src.core.database import start_connection, start_cursor
from .repository import RouteRepository
from src.core.config import settings
from reverse_geocode import search


def fetch_route_service(request_data: dict) -> dict:
    logger.info("FETCH ROUTE SERVICE HIT")

    request_data = {k: v for k, v in request_data.items() if v is not None}

    print(request_data)

    query_filter = {
        "route_id": {"type": "index",
                     "value": request_data.get("route_id"),
                     "table": "Routes"},
        "created_by_company_id": {"type": "index",
                                   "value": request_data.get("company_id"),
                                   "table": "Routes"},
        "created_by_user_id": {"type": "index",
                               "value": request_data.get("user_id"),
                               "table": "Routes"},
        "country": {"type": "index",
                    "value": request_data.get("country"),
                    "table": "Routes"},
        "state": {"type": "index",
                  "value": request_data.get("state"),
                  "table": "Routes"},
        "city": {"type": "index",
                 "value": request_data.get("city"),
                 "table": "Routes"},
        "district": {"type": "index",
                     "value": request_data.get("district"),
                     "table": "Routes"},
        "creation_datetime": {"type": "date_range",
                        "value": (request_data.get("date_range_start"), request_data.get("date_range_end")),
                        "table": "Routes"}
    }

    with start_connection(settings.DB_HOST, settings.DB_USER, settings.DB_PASSWORD, settings.DB_SCHEMA) as conn:
        with start_cursor(conn) as cursor:

            result: dict = RouteRepository.fetch(cursor, query_filter)

    return result

def add_route_service(data: dict):
    logger.info("ADD ROUTE SERVICE HIT")

    route_data: dict = data
    subroutes: list = route_data.pop("subroutes")


    subroutes_data: dict = {}
    for idx, entry in enumerate(subroutes):
        entry_data = list(entry.values())

        subroute_type, address, latitude, longitude = entry_data

        coordinates = (latitude, longitude)

        geocode_search = search([coordinates])[0]

        country = geocode_search['country']
        state = geocode_search['state']
        city = geocode_search['county']
        district = geocode_search['city'] # returns the neighborhood

        subroutes_data[idx+1] = {
            "subroute_type": subroute_type,
            "address": address,
            "longitude": longitude,
            "latitude": latitude,
            "country": country,
            "state": state,
            "city": city,
            "district": district
        }

    route_data["subroutes"] = subroutes_data

    with start_connection(settings.DB_HOST, settings.DB_USER, settings.DB_PASSWORD, settings.DB_SCHEMA) as conn:
        with start_cursor(conn) as cursor:

            route_id = RouteRepository.add(cursor, data)

        conn.commit()

    if route_id:
        return "Route added successfully"

    else:
        return "Route creation failed"

def edit_route_service(request_data: dict):
    logger.info("EDIT ROUTE SERVICE HIT")


    request_data = {k: v for k, v in request_data.items() if v is not None}

    request_route_id: int = request_data.get("route_id")

    query_filter = {
        "route_id": {"type": "index",
                     "value": request_route_id,
                     "table": "Routes"}
    }

    subroutes: dict = request_data.pop("subroutes")

    query_data = {
        "table": "Routes",
        "filter": query_filter,
        "data": request_data
    }

    with start_connection(settings.DB_HOST, settings.DB_USER, settings.DB_PASSWORD, settings.DB_SCHEMA) as conn:
        with start_cursor(conn) as cursor:

            route_data: dict = RouteRepository.fetch(cursor, query_filter)

            if not route_data:
                raise IndexError("Route ID has no data")

            for k, v in subroutes.items():
                request_subroute_id: int = int(k)
                request_data: dict = v
                query_filter = {
                    "route_id": {"type": "index",
                                 "value": request_route_id,
                                 "table": "Routes"},
                    "subroute_id": {"type": "index",
                                    "value": request_subroute_id,
                                    "table": "Routes"}
                }

                query_data = {
                    "table": "Routes",
                    "filter": query_filter,
                    "data": request_data
                }

                RouteRepository.edit(cursor, query_data)

        conn.commit()

def remove_route_service(route_id: int):
    logger.info("REMOVE ROUTE SERVICE HIT")

    query_filter = {
        "table": "Routes",
        "route_id": {"type": "index",
                     "value": route_id,
                     "table": "Routes"}
    }

    query_data = {
        "table": "Routes",
        "filter": query_filter
    }

    with start_connection(settings.DB_HOST, settings.DB_USER, settings.DB_PASSWORD, settings.DB_SCHEMA) as conn:
        with start_cursor(conn) as cursor:
            route_data: dict = RouteRepository.fetch(cursor, query_filter)

            if not route_data:
                raise IndexError("Route ID has no data")

            RouteRepository.remove(cursor, query_data)
            conn.commit()
