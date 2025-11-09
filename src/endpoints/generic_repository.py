from pypika import MySQLQuery, Table, Order
from src.queries.generic import assemble_condition
from src.core.database import Statements
from src.core.logging_config import logger
from src.queries.generic import assemble_condition


ATTACHMENTS = Table("Attachments")
COMPANIES = Table("Companies")
USERS = Table("Users")

def get_last_entry(cursor, target_table: str, target_column: str, condition: dict = None):
    logger.info("GET LAST ENTRY GENERIC REPOSITORY HIT")

    try:
        table = Table(target_table)

        column = getattr(table, target_column)

        if condition:
            stmt = MySQLQuery.from_(table).select(column).where(assemble_condition(condition)).orderby(column, order=Order.desc).limit(1)

        else:
            stmt = MySQLQuery.from_(table).select(column).orderby(column, order=Order.desc).limit(1)

        select_stmt = stmt.get_sql()

        logger.info(f"To execute: {select_stmt}")

        cursor.execute(select_stmt)
        logger.info("Executed")

        return cursor.fetchone()

    except Exception as e:
        print(e)
        return None

def edit(update_data: dict):
    logger.info("EDIT GENERIC REPOSITORY HIT")

    table_name = update_data["table"]
    data = update_data["data"]
    filter_ = update_data.get("filter")

    table = Table(table_name)

    stmt = MySQLQuery.update(table)

    for key, value in data.items():
        stmt = stmt.set(table[key], value)

    if filter_:
        condition = assemble_condition(filter_)
        stmt = stmt.where(condition)


    return stmt.get_sql()


def remove(delete_data: dict):
    logger.info("REMOVE GENERIC REPOSITORY HIT")

    table_name = delete_data["table"]
    filter_ = delete_data["filter"]

    table = Table(table_name)

    condition = assemble_condition(filter_)

    stmt = MySQLQuery.from_(table).where(condition).delete()

    return stmt.get_sql()

