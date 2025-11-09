from .queries import AssembleStatement
from src.core.logging_config import logger
from src.endpoints.generic_repository import get_last_entry
from src.register import Register
from base64 import b64encode
from src.endpoints import generic_repository


class RouteRepository:

    @staticmethod
    def fetch(cursor, query_filter: dict) -> dict | None:
        logger.info("FETCH ROUTE REPOSITORY HIT")

        try:
            select_stmt = AssembleStatement.get_route_data(query_filter)
            logger.info(f"To execute: {select_stmt}")

            cursor.execute(select_stmt)
            logger.info("Executed")

            result = cursor.fetchall()

            if not result:
                return None

            routes: dict = {}
            subroutes_data: dict = {}
            for entry in result:
                (
                    route_id,
                    subroute_id,
                    created_by_company_id,
                    company_name,
                    created_by_user_id,
                    user_name,
                    creation_datetime,
                    subroute_type,
                    address,
                    longitude,
                    latitude,
                    country,
                    state,
                    city,
                    district,
                ) = entry

                if route_id not in routes:
                    routes[route_id] = {
                        "company_id": created_by_company_id,
                        "company_name": company_name,
                        "user_id": created_by_user_id,
                        "user_name": user_name,
                        "creation_datetime": str(creation_datetime),
                        "subroutes": {}
                    }

                routes[route_id]["subroutes"][subroute_id] = {
                    "subroute_type": subroute_type,
                    "address": address,
                    "latitude": latitude,
                    "longitude": longitude,
                    "country": country,
                    "state": state,
                    "city": city,
                    "district": district,
                }

            return routes

        except IndexError:
            return None


    @staticmethod
    def add(cursor, data: dict):
        logger.info("ADD ROUTE REPOSITORY HIT")
        """
        {
            'company_id': 123,
            'user_id': 42,
            'creation_datetime': '2025-10-31 23:02:41.255466',
            'subroutes': {
                1: {
                    'subroute_type': 'start',
                    'address': 'A Street',
                    'longitude': -46.6333,
                    'latitude': -23.5505
                },
                2: {
                    'subroute_type': 'middle',
                    'address': 'B Street',
                    'longitude': -46.62,
                    'latitude': -23.56
                },
                3: {
                    'subroute_type': 'end',
                    'address': 'C Street',
                    'longitude': -46.61,
                    'latitude': -23.57
                }
            }
        }
        """
        last_route_id = get_last_entry(cursor, "Routes", "route_id")[0]
        if last_route_id is None:
            route_id = 1
        else:
            route_id = last_route_id + 1

        company_id = data['company_id']
        user_id = data['user_id']
        creation_datetime = data['creation_datetime']
        subroutes = data['subroutes']

        values = []
        for subroute_id, entry in subroutes.items():
            values.append((route_id, subroute_id, company_id, user_id, creation_datetime, entry['subroute_type'], entry['address'], entry['longitude'], entry['latitude'], entry['country'], entry['state'], entry['city'], entry['district']))
        try:
            insert_stmt = AssembleStatement.add_route(values)
            logger.info(f"To execute: {insert_stmt}")

            cursor.execute(insert_stmt)
            logger.info("Executed")

        except Exception as e:
            print(e)
            return None

        return cursor.lastrowid

    @staticmethod
    def edit(cursor, data: dict):
        logger.info("EDIT ROUTE REPOSITORY HIT")

        try:
            update_stmt = generic_repository.edit(data)
            logger.info(f"To execute: {update_stmt}")

            cursor.execute(update_stmt)
            logger.info("Executed")

        except Exception as e:
            print(e)
            return None


    @staticmethod
    def remove(cursor, data: dict):
        logger.info("REMOVE ROUTE REPOSITORY HIT")

        try:
            remove_stmt = generic_repository.remove(data)
            logger.info(f"To execute: {remove_stmt}")

            cursor.execute(remove_stmt)
            logger.info("Executed")

        except Exception as e:
            logger.info("Error during edit:", e)


