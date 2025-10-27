from pypika import MySQLQuery, Table
from src.queries.generic import assemble_condition

ATTACHMENTS = Table("Attachments")
COMPANIES = Table("Companies")
USERS = Table("Users")


def get_data(query_filter) -> str:
    query = (
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

    return query.get_sql()
