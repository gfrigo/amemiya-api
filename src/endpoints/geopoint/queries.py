from pypika import MySQLQuery, Table
from src.queries.generic import assemble_condition

GEOPOINTS = Table("Geopoints")
COMPANIES = Table("Companies")
USERS = Table("Users")

class AssembleStatement:

    @staticmethod
    def get_geopoint_data(query_filter) -> str:
        stmt = (
            MySQLQuery.from_(GEOPOINTS).select(
                GEOPOINTS.geopoint_id,
                GEOPOINTS.company_id,
                COMPANIES.company_name,
                GEOPOINTS.point_id,
                GEOPOINTS.user_id,
                USERS.user_name,
                GEOPOINTS.label,
                GEOPOINTS.longitude,
                GEOPOINTS.latitude,
                GEOPOINTS.geopoint_type,
                GEOPOINTS.country,
                GEOPOINTS.state,
                GEOPOINTS.city,
                GEOPOINTS.district
            )
            .left_join(COMPANIES).on(GEOPOINTS.company_id == COMPANIES.company_id)
            .left_join(USERS).on(GEOPOINTS.user_id == USERS.user_id)
            .where(assemble_condition(query_filter))
        )

        return stmt.get_sql()

    @staticmethod
    def add_geopoint(values: list) -> str:
        columns = (
            'company_id', 'point_id', 'user_id', 'label',
            'longitude', 'latitude', 'location', 'geopoint_type',
            'country', 'state', 'city', 'district'
        )

        company_id, user_id, label, longitude, latitude, geopoint_type, country, state, city, district, point_id = values
        location_stmt = f"ST_SRID(POINT({longitude},{latitude}),4326)"
        row_stmt = f"({company_id},{point_id},{user_id},'{label}',{longitude},{latitude}, {location_stmt},'{geopoint_type}', '{country}', '{state}', '{city}', '{district}')"

        insert_stmt = f"INSERT INTO `Geopoints` ({', '.join(columns)}) VALUES {row_stmt};"
        return insert_stmt

    @staticmethod
    def edit_attachment(attachment_id, data: dict) -> str:
        elements = [f"{key} = %s" for key, value in data.items() if value is not None]
        stmt = f"UPDATE `Attachments` SET {', '.join(elements)} WHERE attachment_id = {attachment_id}"

        return stmt
