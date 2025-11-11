from pypika import MySQLQuery, Table
from src.queries.generic import assemble_condition

REFUELINGS = Table("Refuelings")
ATTACHMENTS = Table("Attachments")
VEHICLES = Table("Vehicles")
COMPANIES = Table("Companies")
USERS = Table("Users")

class AssembleStatement:

    @staticmethod
    def get_refueling_data(query_filter) -> str:
        stmt = (
            MySQLQuery.from_(REFUELINGS).select(
                REFUELINGS.refueling_id,
                REFUELINGS.company_id,
                COMPANIES.company_name,
                REFUELINGS.user_id,
                USERS.user_name,
                REFUELINGS.vehicle_id,
                VEHICLES.vehicle_name,
                VEHICLES.license_plate,
                VEHICLES.brand,
                VEHICLES.model,
                VEHICLES.year,
                REFUELINGS.attachment_id,
                ATTACHMENTS.file_data,
                ATTACHMENTS.file_type,
                ATTACHMENTS.upload_date,
                REFUELINGS.refueling_type,
                REFUELINGS.refueling_origin,
                REFUELINGS.refueling_station,
                REFUELINGS.current_kilometrage,
                REFUELINGS.refueling_volume,
                REFUELINGS.cost,
                REFUELINGS.refueling_date
            )
            .left_join(COMPANIES).on(REFUELINGS.company_id == COMPANIES.company_id)
            .left_join(USERS).on(REFUELINGS.user_id == USERS.user_id)
            .left_join(VEHICLES).on(REFUELINGS.vehicle_id == VEHICLES.vehicle_id)
            .left_join(ATTACHMENTS).on(REFUELINGS.attachment_id == ATTACHMENTS.attachment_id)
            .where(assemble_condition(query_filter))
        )

        return stmt.get_sql()

    @staticmethod
    def add_refueling(data: dict) -> str:
        stmt = MySQLQuery.into(REFUELINGS).columns(*data.keys()).insert(*data.values())

        return stmt.get_sql()
