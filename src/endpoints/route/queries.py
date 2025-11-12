
from pypika import MySQLQuery, Table

from src.endpoints.generic_repository import assemble_condition

ROUTES = Table("Routes")
COMPANIES = Table("Companies")
USERS = Table("Users")

class AssembleStatement:

    @staticmethod
    def get_route_data(query_filter) -> str:
        stmt = (
            MySQLQuery.from_(ROUTES).select(
                ROUTES.route_id,
                ROUTES.subroute_id,
                ROUTES.created_by_company_id,
                COMPANIES.company_name,
                ROUTES.created_by_user_id,
                USERS.user_name,
                ROUTES.creation_datetime,
                ROUTES.subroute_type,
                ROUTES.address,
                ROUTES.longitude,
                ROUTES.latitude,
                ROUTES.country,
                ROUTES.state,
                ROUTES.city,
                ROUTES.district
            )
            .left_join(COMPANIES).on(ROUTES.created_by_company_id == COMPANIES.company_id)
            .left_join(USERS).on(ROUTES.created_by_user_id == USERS.user_id)
            .where(assemble_condition(query_filter))
        )

        return stmt.get_sql()

    @staticmethod
    def add_route(values: list) -> str:
        columns = (
            'route_id', 'subroute_id', 'created_by_company_id', 'created_by_user_id',
            'creation_datetime', 'subroute_type', 'address', 'longitude', 'latitude', 'location',
            'country', 'state', 'city', 'district'
        )

        values_sql = []
        for v in values:
            route_id, subroute_id, company_id, user_id, creation_datetime, subroute_type, address, longitude, latitude, country, state, city, district = v
            location_stmt = f"ST_SRID(POINT({longitude},{latitude}),4326)"
            row_stmt = f"({route_id},{subroute_id},{company_id},{user_id},'{creation_datetime}','{subroute_type}','{address}',{longitude}, {latitude}, {location_stmt}, '{country}', '{state}', '{city}', '{district}')"
            values_sql.append(row_stmt)

        insert_stmt = f"INSERT INTO `Routes` ({', '.join(columns)}) VALUES {', '.join(values_sql)};"
        return insert_stmt

    @staticmethod
    def edit_attachment(attachment_id, data: dict) -> str:
        elements = [f"{key} = %s" for key, value in data.items() if value is not None]
        stmt = f"UPDATE `Attachments` SET {', '.join(elements)} WHERE attachment_id = {attachment_id}"

        return stmt
