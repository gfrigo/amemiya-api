from pypika import MySQLQuery, Table, Order

from src.core.config import logger
from functools import reduce
from operator import and_
from pypika import Table


def assemble_individual_condition(label, specs):
    if not isinstance(specs, dict):
        return None

    element_type = specs.get("type")
    element_value = specs.get("value")
    element_table = Table(specs.get("table"))

    if element_type == "index":
        if element_value is None:
            return None
        return getattr(element_table, label) == element_value

    elif element_type == "date_range":
        start, end = element_value
        if start is None and end is None:
            return None
        start = "0001-01-01" if start is None else start
        end = "9999-12-31" if end is None else end
        return getattr(element_table, label).between(start, end)

    elif element_type == "value_range":
        start, end = element_value
        if start is None and end is None:
            return None
        start = 0 if start is None else start
        end = 999_999_999 if end is None else end
        return getattr(element_table, label).between(start, end)

    elif element_type == "similarity":
        if element_value is None:
            return None
        return getattr(element_table, label).like(f"%{element_value}%")


def assemble_condition(query_filter: dict):
    conditions = []

    for k, v in query_filter.items():
        stmt = assemble_individual_condition(k, v)

        if stmt is not None:
            conditions.append(stmt)

    if not conditions:
        return None

    return reduce(and_, conditions)



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

def fetch(cursor, target_table: str, target_column: str = None, condition: dict = None):
    logger.info("FETCH GENERIC REPOSITORY HIT")

    table = Table(target_table)

    if target_column:
        column = getattr(table, target_column)
        stmt = MySQLQuery.from_(table).select(column)
    else:
        stmt = MySQLQuery.from_(table)

    if condition:
        stmt = stmt.where(assemble_condition(condition))

    cursor.execute(stmt.get_sql())

    return cursor.fetchall()

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

