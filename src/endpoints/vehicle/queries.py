from pypika import MySQLQuery, Table
from src.queries.generic import assemble_condition

VEHICLES = Table("Vehicles")
USERS = Table("Users")
COMPANIES = Table("Companies")

class AssembleStatement:

    @staticmethod
    def get_vehicle_data(query_filter) -> str:
        stmt = (
            MySQLQuery.from_(VEHICLES).select(
                VEHICLES.vehicle_id,
                VEHICLES.vehicle_name,
                VEHICLES.license_plate,
                VEHICLES.brand,
                VEHICLES.model,
                VEHICLES.year,
                VEHICLES.notes,
                VEHICLES.company_id,
                COMPANIES.company_name,
                VEHICLES.last_user_id,
                USERS.user_name,
                VEHICLES.last_used,
                VEHICLES.active_vehicle
            )
            .left_join(USERS).on(VEHICLES.last_user_id == USERS.user_id)
            .left_join(COMPANIES).on(VEHICLES.company_id == COMPANIES.company_id)
            .where(assemble_condition(query_filter))
        )

        return stmt.get_sql()

    @staticmethod
    def add_vehicle(columns: tuple, values: tuple) -> str:

        stmt = MySQLQuery.into(VEHICLES).columns(*columns).insert(*values)

        return stmt.get_sql()