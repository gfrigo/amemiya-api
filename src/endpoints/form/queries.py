from pypika import MySQLQuery, Table

from src.endpoints.generic_repository import assemble_condition

FORMS = Table("Forms")
COMPANIES = Table("Companies")
USERS = Table("Users")
DELIVERIES = Table("Deliveries")

class AssembleStatement:

    @staticmethod
    def get_form_data(query_filter) -> str:
        stmt = (
            MySQLQuery.from_(FORMS).select(
                FORMS.form_id,
                FORMS.company_id,
                COMPANIES.company_name,
                FORMS.user_id,
                USERS.user_name,
                FORMS.delivery_id,
                DELIVERIES.delivery_code,
                FORMS.description,
                FORMS.was_delivered,
                FORMS.had_problem,
                FORMS.problem_description,
                FORMS.who_received,
                FORMS.creation_datetime,
                FORMS.notes
            )
            .left_join(USERS).on(FORMS.user_id == USERS.user_id)
            .left_join(COMPANIES).on(FORMS.company_id == COMPANIES.company_id)
            .left_join(DELIVERIES).on(FORMS.delivery_id == DELIVERIES.delivery_id)
            .where(assemble_condition(query_filter))
        )

        return stmt.get_sql()

    @staticmethod
    def add_form(columns: tuple, values: tuple) -> str:

        stmt = MySQLQuery.into(FORMS).columns(*columns).insert(*values)

        return stmt.get_sql()