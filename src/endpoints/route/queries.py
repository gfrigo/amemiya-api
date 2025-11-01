from pypika import MySQLQuery, Table
from src.queries.generic import assemble_condition

ROUTES = Table("Routes")
COMPANIES = Table("Companies")
USERS = Table("Users")

class AssembleStatement:

    '''@staticmethod
    def get_attachment_data(query_filter) -> str:
        stmt = (
            MySQLQuery.from_(ATTACHMENTS).select(
                ATTACHMENTS.attachment_id,
                COMPANIES.company_name,
                USERS.user_name,
                ATTACHMENTS.file_data,
                ATTACHMENTS.file_type,
                ATTACHMENTS.attachment_type,
                ATTACHMENTS.upload_date
            )
            .left_join(COMPANIES).on(ATTACHMENTS.uploaded_by_company_id == COMPANIES.company_id)
            .left_join(USERS).on(ATTACHMENTS.uploaded_by_user_id == USERS.user_id)
            .where(assemble_condition(query_filter))
        )

        return stmt.get_sql()'''

    @staticmethod
    def add_route(values: list) -> str:
        columns = (
            'route_id', 'subroute_id', 'created_by_company_id', 'created_by_user_id',
            'creation_datetime', 'subroute_type', 'address', 'longitude', 'latitude', 'location'
        )

        values_sql = []
        for v in values:
            route_id, subroute_id, company_id, user_id, creation_datetime, subroute_type, address, longitude, latitude = v
            location_stmt = f"ST_SRID(POINT({longitude},{latitude}),4326)"
            row_stmt = f"({route_id},{subroute_id},{company_id},{user_id},'{creation_datetime}','{subroute_type}','{address}',{longitude},{latitude},{location_stmt})"
            values_sql.append(row_stmt)

        insert_stmt = f"INSERT INTO `Routes` ({', '.join(columns)}) VALUES {', '.join(values_sql)};"
        return insert_stmt

    @staticmethod
    def edit_attachment(attachment_id, data: dict) -> str:
        elements = [f"{key} = %s" for key, value in data.items() if value is not None]
        stmt = f"UPDATE `Attachments` SET {", ".join(elements)} WHERE attachment_id = {attachment_id}"

        return stmt
