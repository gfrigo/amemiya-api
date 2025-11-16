from pypika import MySQLQuery, Table

from src.endpoints.generic_repository import assemble_condition

USERS = Table("Users")
ROLES = Table("Roles")
COMPANIES = Table("Companies")
ATTACHMENTS = Table("Attachments")

class AssembleStatement:

    @staticmethod
    def get_all_users(query_filter) -> str:
        stmt = (
            MySQLQuery.from_(USERS).select(
                USERS.user_id,
                USERS.user_name,
                USERS.inner_register,
                USERS.email,
                USERS.telephone,
                USERS.role_id,
                ROLES.role_name,
                USERS.company_id,
                COMPANIES.company_name
            )
            .left_join(ROLES).on(USERS.role_id == ROLES.role_id)
            .left_join(COMPANIES).on(USERS.company_id == COMPANIES.company_id)
            .where(assemble_condition(query_filter))
        )

        return stmt.get_sql()

    @staticmethod
    def get_user_data(query_filter) -> str:
        stmt = (
            MySQLQuery.from_(USERS).select(
                USERS.user_id,
                USERS.user_name,
                USERS.inner_register,
                USERS.email,
                USERS.telephone,
                USERS.role_id,
                ROLES.role_name,
                USERS.admin,
                USERS.company_id,
                COMPANIES.company_name,
                USERS.profile_picture_id,
                ATTACHMENTS.file_data
            )
            .left_join(ROLES).on(USERS.role_id == ROLES.role_id)
            .left_join(COMPANIES).on(USERS.company_id == COMPANIES.company_id)
            .left_join(ATTACHMENTS).on(USERS.profile_picture_id == ATTACHMENTS.attachment_id)
            .where(assemble_condition(query_filter))
        )

        return stmt.get_sql()

    @staticmethod
    def add_user(columns: tuple, values: tuple) -> str:

        stmt = MySQLQuery.into(USERS).columns(*columns).insert(*values)

        return stmt.get_sql()