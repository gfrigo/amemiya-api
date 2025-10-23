from src.core.logging_config import logger
from src.register import Register
from pypika import MySQLQuery, Table, Parameter
from src.map import fetch, add, edit, remove


class VehicleRepository:
    vehicle_table = Table("Vehicle")

    @classmethod
    def fetch(cls, cursor, data: dict, selection: list | None) -> list | None:
        logger.info("FETCH VEHICLE REPOSITORY HIT")
        company_id: int = data["company_id"]
        vehicle_id: int = data["vehicle_id"]

        if not company_id and not vehicle_id:
            return None

        if selection:
            columns = [getattr(cls.vehicle_table, column) for column in selection]
        else:
            columns = [cls.vehicle_table.star]

        if vehicle_id:
            query = MySQLQuery.from_(cls.vehicle_table).select(*columns).where(
                cls.vehicle_table.vehicle_id == vehicle_id)
        else:
            query = MySQLQuery.from_(cls.vehicle_table).select(*columns).where(
                cls.vehicle_table.company_id == company_id)

        query_str = query.get_sql()

        logger.info(f"To execute: {query_str}")

        cursor.execute(query_str)
        result = cursor.fetchall()

        return result


    @classmethod
    def add(cls, cursor, data: dict):
        logger.info("ADD VEHICLE REPOSITORY HIT")

        values: tuple = (
            data["company_id"],
            data["name"],
            data["license_plate"],
            data["brand"],
            data["model"],
            data["year"]
        )

        mapping = add.get("vehicle")
        if not mapping:
            raise KeyError("Unknown entity 'vehicle'")

        query = MySQLQuery.into(cls.vehicle_table).columns([
            "company_id",
            "name",
            "license_plate",
            "brand",
            "model",
            "year"
        ]).insert(*[Parameter("%s")]*6)
        query_str = query.get_sql()

        cursor.execute(query_str, values)

    @classmethod
    def edit(cls, cursor, data: dict):
        logger.info("EDIT VEHICLE REPOSITORY HIT")

        key = f"vehicle_id = {data['vehicle_id']}"
        Register.edit(cursor, "vehicle", data, key)

    @classmethod
    def remove(cls, cursor, data: dict):
        logger.info("REMOVE VEHICLE REPOSITORY HIT")

        query = MySQLQuery.from_(cls.vehicle_table).delete().where(cls.vehicle_table.vehicle_id == data["vehicle_id"])
        query_str = query.get_sql()

        logger.debug(f"To execute: {query_str}")

        cursor.execute(query_str)

