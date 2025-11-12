from pypika import MySQLQuery, Table

from src.endpoints.generic_repository import assemble_condition

MAINTENANCES = Table("Maintenances")
ATTACHMENTS = Table("Attachments")
VEHICLES = Table("Vehicles")
COMPANIES = Table("Companies")
USERS = Table("Users")

class AssembleStatement:

    @staticmethod
    def get_maintenance_data(query_filter) -> str:
        stmt = (
            MySQLQuery.from_(MAINTENANCES).select(
                MAINTENANCES.maintenance_id,
                MAINTENANCES.company_id,
                COMPANIES.company_name,
                MAINTENANCES.user_id,
                USERS.user_name,
                MAINTENANCES.vehicle_id,
                VEHICLES.vehicle_name,
                VEHICLES.license_plate,
                VEHICLES.brand,
                VEHICLES.model,
                VEHICLES.year,
                MAINTENANCES.attachment_id,
                ATTACHMENTS.file_data,
                ATTACHMENTS.file_type,
                ATTACHMENTS.upload_date,
                MAINTENANCES.maintenance_type,
                MAINTENANCES.maintenance_origin,
                MAINTENANCES.maintenance_responsible,
                MAINTENANCES.cost,
                MAINTENANCES.maintenance_date
            )
            .left_join(COMPANIES).on(MAINTENANCES.company_id == COMPANIES.company_id)
            .left_join(USERS).on(MAINTENANCES.user_id == USERS.user_id)
            .left_join(VEHICLES).on(MAINTENANCES.vehicle_id == VEHICLES.vehicle_id)
            .left_join(ATTACHMENTS).on(MAINTENANCES.attachment_id == ATTACHMENTS.attachment_id)
            .where(assemble_condition(query_filter))
        )

        return stmt.get_sql()

    @staticmethod
    def add_maintenance(data: dict) -> str:
        stmt = MySQLQuery.into(MAINTENANCES).columns(*data.keys()).insert(*data.values())

        return stmt.get_sql()
