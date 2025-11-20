from src.core.config import logger
from src.endpoints import generic_repository
from src.endpoints.generic_repository import get_last_entry
from .queries import AssembleStatement


class GeopointRepository:

    @staticmethod
    def fetch(cursor, query_filter: dict) -> dict | None:
        logger.info("FETCH GEOPOINT REPOSITORY HIT")

        request_geopoint_id = query_filter.get("geopoint_id")

        if request_geopoint_id:
            request_geopoint_id = request_geopoint_id.get("value")

        try:
            select_stmt = AssembleStatement.get_geopoint_data(query_filter)
            logger.info(f"To execute: {select_stmt}")

            cursor.execute(select_stmt)
            logger.info("Executed")

            result = cursor.fetchall()
            if not result:
                return None

            origin_points: list = []
            destiny_points: list = []
            for entry in result:
                (
                    geopoint_id,
                    company_id,
                    company_name,
                    point_id,
                    user_id,
                    user_name,
                    label,
                    longitude,
                    latitude,
                    geopoint_type,
                    country,
                    state,
                    city,
                    district
                ) = entry

                geopoint_data = {
                    "geopoint_id": geopoint_id,
                    "company_id": company_id,
                    "company_name": company_name,
                    "point_id": point_id,
                    "user_id": user_id,
                    "user_name": user_name,
                    "label": label,
                    "latitude": latitude,
                    "longitude": longitude,
                    "country": country,
                    "state": state,
                    "city": city,
                    "district": district
                }

                if request_geopoint_id:
                    return geopoint_data

                if geopoint_type == "origin":
                    origin_points.append(geopoint_data)
                elif geopoint_type == "destiny":
                    destiny_points.append(geopoint_data)

            geopoints: dict = {
                "origin": origin_points if origin_points else None,
                "destiny": destiny_points if destiny_points else None
            }

            return geopoints

        except IndexError:
            return None


    @staticmethod
    def add(cursor, data: dict):
        logger.info("ADD GEOPOINT REPOSITORY HIT")

        query_filter = {
            "company_id": {"type": "index",
                         "value": data.get("company_id"),
                         "table": "Geopoints"}
        }

        raw_last_entry = get_last_entry(cursor, "Geopoints", "point_id", query_filter)
        last_point_id = 0 if raw_last_entry is None else raw_last_entry[0]

        data["point_id"] = 1 if last_point_id is None else last_point_id + 1

        values = list(data.values())

        try:
            insert_stmt = AssembleStatement.add_geopoint(values)
            logger.info(f"To execute: {insert_stmt}")

            cursor.execute(insert_stmt)
            logger.info("Executed")

        except Exception as e:
            print(e)
            return None

        return cursor.lastrowid

    @staticmethod
    def edit(cursor, data: dict):
        logger.info("EDIT GEOPOINT REPOSITORY HIT")

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
        logger.info("REMOVE GEOPOINT REPOSITORY HIT")

        try:
            remove_stmt = generic_repository.remove(data)
            logger.info(f"To execute: {remove_stmt}")

            cursor.execute(remove_stmt)
            logger.info("Executed")

        except Exception as e:
            logger.info("Error during edit:", e)


