from .queries import AssembleStatement
from src.core.logging_config import logger
from src.endpoints.generic_repository import get_last_entry
from src.register import Register
from base64 import b64encode


class RouteRepository:

    @staticmethod
    def fetch(cursor, query_filter: dict) -> dict | None:
        logger.info("FETCH ATTACHMENT REPOSITORY HIT")

        try:
            select_stmt = AssembleStatement.get_attachment_data(query_filter)
            logger.info(f"To execute: {select_stmt}")

            cursor.execute(select_stmt)
            logger.info("Executed")

            result = cursor.fetchall()

            if not result:
                return None

            data: dict = {}
            for entry in result:
                attachment_id, company_name, user_name, file_data, file_type, attachment_type, upload_date = entry

                encoded_file_data = b64encode(file_data).decode("utf-8")

                file_name = f"test_output.{file_type}"
                with open(file_name, "wb") as f:
                    f.write(file_data)

                data[attachment_id] = {
                    "company_name": company_name,
                    "user_name": user_name,
                    "file_data": encoded_file_data,
                    "file_type": file_type,
                    "attachment_type": attachment_type,
                    "upload_date": upload_date
                }

            return data

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
        last_route_id = get_last_entry(cursor, "Routes", "route_id")
        if last_route_id is None:
            route_id = 1
        else:
            route_id = last_route_id + 1

        company_id = data['company_id']
        user_id = data['user_id']
        creation_datetime = data['creation_datetime']
        subroutes = data['subroutes']

        values = []
        print(subroutes)
        for subroute_id, entry in subroutes.items():
            values.append((route_id, subroute_id, company_id, user_id, creation_datetime, entry['subroute_type'], entry['address'], entry['longitude'], entry['latitude']))

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
    def edit(cursor, attachment_id, data: dict):
        logger.info("EDIT ATTACHMENT REPOSITORY HIT")

        try:
            update_stmt = AssembleStatement.edit_attachment(attachment_id, data)
            logger.info(f"To execute: {update_stmt}")

            cursor.execute(update_stmt, tuple(v for v in data.values() if v is not None))
            logger.info("Executed")

        except Exception as e:
            print(e)
            return None


