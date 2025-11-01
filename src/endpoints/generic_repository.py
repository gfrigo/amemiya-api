from pypika import MySQLQuery, Table, Order
from src.queries.generic import assemble_condition
from src.core.database import Statements
from src.core.logging_config import logger

ATTACHMENTS = Table("Attachments")
COMPANIES = Table("Companies")
USERS = Table("Users")

logger.info("GENERIC REPOSITORY HIT")

def get_last_entry(cursor, target_table: str, target_column: str):
    logger.info("GET LAST ENTRY GENERIC REPOSITORY HIT")

    try:
        table = Table(target_table)

        column = getattr(table, target_column)

        stmt = MySQLQuery.from_(table).select(column).orderby(column, order=Order.desc).limit(1)
        select_stmt = stmt.get_sql()

        logger.info(f"To execute: {select_stmt}")

        cursor.execute(select_stmt)
        logger.info("Executed")

        return cursor.fetchone()

    except Exception as e:
        print(e)
        return None


def remove(cursor, query_filter: dict):
    logger.info("REMOVE GENERIC REPOSITORY HIT")

    try:
        stmt = MySQLQuery.from_(query_filter["table"]).where(assemble_condition(query_filter)).delete()
        delete_stmt = stmt.get_sql()

        logger.info(f"To execute: {delete_stmt}")

        cursor.execute(delete_stmt)
        logger.info("Executed")

    except Exception as e:
        print(e)
        return None
