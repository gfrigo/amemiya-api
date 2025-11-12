from operator import and_
from pypika import MySQLQuery, Table

from src.endpoints.generic_repository import assemble_condition

DELIVERIES = Table("Deliveries")
COMPANIES = Table("Companies")
USERS = Table("Users")
VEHICLES = Table("Vehicles")

class AssembleStatement:

    @staticmethod
    def get_delivery_data(query_filter: dict) -> str:
        stmt = (
            MySQLQuery.from_(DELIVERIES).select(
                DELIVERIES.delivery_id,
                DELIVERIES.company_id,
                COMPANIES.company_name,
                DELIVERIES.user_id,
                USERS.user_name,
                DELIVERIES.vehicle_id,
                VEHICLES.vehicle_name,
                VEHICLES.license_plate,
                VEHICLES.brand,
                VEHICLES.model,
                VEHICLES.year,
                DELIVERIES.delivery_code,
                DELIVERIES.payload_item,
                DELIVERIES.payload_quantity,
                DELIVERIES.payload_quantity_unit,
                DELIVERIES.payload_weight,
                DELIVERIES.estimated_delivery_time,
                DELIVERIES.start_time,
                DELIVERIES.start_label,
                DELIVERIES.start_latitude,
                DELIVERIES.start_longitude,
                DELIVERIES.start_city,
                DELIVERIES.start_district,
                DELIVERIES.finish_time,
                DELIVERIES.end_label,
                DELIVERIES.end_latitude,
                DELIVERIES.end_longitude,
                DELIVERIES.end_city,
                DELIVERIES.end_district,
                DELIVERIES.delivery_status
            )
            .left_join(COMPANIES).on(DELIVERIES.company_id == COMPANIES.company_id)
            .left_join(USERS).on(DELIVERIES.user_id == USERS.user_id)
            .left_join(VEHICLES).on(DELIVERIES.vehicle_id == VEHICLES.vehicle_id)
            .where(assemble_condition(query_filter))
        )

        return stmt.get_sql()

    @staticmethod
    def add_delivery(data: dict) -> str:
        stmt = MySQLQuery.into(DELIVERIES).columns(*data.keys()).insert(*data.values())

        return stmt.get_sql()