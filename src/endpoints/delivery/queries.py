#pylint: disable-all
from pypika import MySQLQuery, Table

ROUTES = Table("Routes")
COMPANIES = Table("Companies")
DELIVERY = Table("Delivery")


def get_data(delivery_id: int) -> str:
    query = (
        MySQLQuery.from_(DELIVERY).select(
            DELIVERY.delivery_id,
            DELIVERY.user_id,
            DELIVERY.vehicle_id,
            DELIVERY.route_id,
            DELIVERY.finish_time,
            DELIVERY.load_name,
            DELIVERY.start_time,
            DELIVERY.status
            
        )
        .where(DELIVERY.delivery_id == delivery_id)
    )

    return str(query)