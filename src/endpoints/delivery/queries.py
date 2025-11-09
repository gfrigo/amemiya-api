# pylint: disable-all
from pypika import MySQLQuery, Table
from operator import and_
from src.queries.generic import assemble_condition


ROUTES = Table("Routes")
COMPANIES = Table("Companies")
DELIVERY = Table("Delivery")

def get_data(query_filter: dict) -> str:
    query = (
        MySQLQuery
        .from_(DELIVERY)
        .join(ROUTES)
        .on(DELIVERY.route_id == ROUTES.route_id)
        .join(COMPANIES)
        .on(ROUTES.created_by_company_id == COMPANIES.company_id)
        .select(
            DELIVERY.delivery_id,
            DELIVERY.route_id,
            DELIVERY.vehicle_id,
            DELIVERY.start_time,
            DELIVERY.finish_time,
            DELIVERY.load_name,
            ROUTES.address,
            COMPANIES.company_name
        )
        .where(assemble_condition(query_filter))
    )

    return query.get_sql()