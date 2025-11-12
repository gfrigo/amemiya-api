from pypika import MySQLQuery, Table

from src.endpoints.generic_repository import assemble_condition

INVOICES = Table("Invoices")
ATTACHMENTS = Table("Attachments")
COMPANIES = Table("Companies")
USERS = Table("Users")

class AssembleStatement:

    @staticmethod
    def get_invoice_data(query_filter) -> str:
        stmt = (
            MySQLQuery.from_(INVOICES).select(
                INVOICES.invoice_id,
                INVOICES.company_id,
                COMPANIES.company_name,
                INVOICES.user_id,
                USERS.user_name,
                INVOICES.attachment_id,
                ATTACHMENTS.file_data,
                ATTACHMENTS.file_type,
                ATTACHMENTS.upload_date,
                INVOICES.cost,
                INVOICES.purchase_type,
                INVOICES.invoice_origin,
                INVOICES.invoice_number,
                INVOICES.invoice_series,
                INVOICES.emission_date
            )
            .left_join(COMPANIES).on(INVOICES.company_id == COMPANIES.company_id)
            .left_join(USERS).on(INVOICES.user_id == USERS.user_id)
            .left_join(ATTACHMENTS).on(INVOICES.attachment_id == ATTACHMENTS.attachment_id)
            .where(assemble_condition(query_filter))
        )

        return stmt.get_sql()

    @staticmethod
    def add_invoice(data: dict) -> str:
        stmt = MySQLQuery.into(INVOICES).columns(*data.keys()).insert(*data.values())

        return stmt.get_sql()
