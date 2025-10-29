from pypika import MySQLQuery, Table
from src.queries.generic import assemble_condition

ATTACHMENTS = Table("Attachments")
COMPANIES = Table("Companies")
USERS = Table("Users")

class AssembleStatement:

    @staticmethod
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

        return stmt.get_sql()

    @staticmethod
    def add_attachment(data: dict) -> str:
        columns = ", ".join(data.keys())
        placeholders = ", ".join(["%s"] * len(data))
        stmt = f"INSERT INTO `Attachments` (`uploaded_by_company_id`, `uploaded_by_user_id`, `file_data`, `file_type`, `attachment_type`, `upload_date`) VALUES ({placeholders})"

        return stmt
