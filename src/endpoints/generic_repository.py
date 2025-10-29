from pypika import MySQLQuery, Table
from src.queries.generic import assemble_condition
from src.core.database import Statements
from src.core.logging_config import logger

ATTACHMENTS = Table("Attachments")
COMPANIES = Table("Companies")
USERS = Table("Users")

logger.info("GENERIC REPOSITORY HIT")

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
