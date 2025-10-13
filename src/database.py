import mysql.connector
from contextlib import contextmanager


@contextmanager
def start_connection(db_host:str, db_user:str, db_password:str, db_schema:str=None):
    conn = mysql.connector.connect(
        host=db_host,
        user=db_user,
        password=db_password,
        database=db_schema
    )
    try:
        yield conn
    finally:
        conn.close()


@contextmanager
def start_cursor(conn):
    cursor = conn.cursor()
    try:
        yield cursor
    finally:
        cursor.close()


def insert(cursor, table: str, fields: tuple, values: list[tuple] | tuple) -> None:
    if not table:
        raise ValueError("No table has been provided.")

    if not isinstance(fields, (tuple, list)) or not fields:
        raise ValueError("Fields must be a non-empty tuple or list.")

    if not isinstance(values, (tuple, list)) or not values:
        raise ValueError("Values must be a non-empty tuple or list.")

    fields_length = len(fields)
    if isinstance(values, tuple):
        values_length = len(values)

        if fields_length != values_length:
            raise ValueError("Fields and Values have different lengths")

    elif isinstance(values, list):
        for i in range(1, len(values), 1):
            if not isinstance(values[i-1], tuple) or not isinstance(values[i], tuple):
                raise TypeError("Not all elements inside Values are tuples")

            if len(values[i-1]) != len(values[i]) or len(values[i-1]) != fields_length or len(values[i]) != fields_length:
                raise ValueError("Not all elements inside Values have the same length or have different lengths of Fields")

    insert_stmt: str = f"INSERT INTO {table} ({', '.join(fields)}) VALUES ({', '.join(['%s'] * fields_length)})"

    print(insert_stmt)
    print(values)

    if isinstance(values, tuple):
        cursor.execute(insert_stmt, values)

    elif isinstance(values, list):
        cursor.executemany(insert_stmt, values)

def query_from_table(cursor, table: str, selection: str | tuple = "*", where: str | tuple = "", extra: str = ""):
    if not table:
        raise ValueError("No table has been provided.")

    if isinstance(selection, tuple):
        selection: str = ", ".join(selection)
    elif isinstance(selection, str):
        selection: str = selection

    if where:
        if isinstance(where, tuple):
            where: str | None = " WHERE " + " AND ".join(where)

        elif isinstance(where, str):
            where: str | None = " WHERE " + where

    query_stmt: str = f"SELECT {selection} FROM {table}{where}{extra};"

    print(query_stmt)

    cursor.execute(query_stmt)

    return cursor.fetchall()

def query_from_procedure():
    ...