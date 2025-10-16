import mysql.connector
from contextlib import contextmanager


class Statements:
    @staticmethod
    def get_where(stmt: str | tuple) -> str:
        if not stmt:
            return ""

        if isinstance(stmt, tuple):
            if len(stmt) == 1:
                if not stmt[0]:
                    return ""

                else:
                    return " WHERE " + stmt[0]

            else:
                return " WHERE " + " AND ".join(stmt)

        elif isinstance(stmt, str):
            return " WHERE " + stmt

        else:
            return ""

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
        raise ValueError("Fields must be a non-empty tuple.")

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

    insert_stmt: str = f"INSERT INTO {table} ({', '.join(fields)}) VALUES ({', '.join(['%s'] * fields_length)});"

    print(insert_stmt)
    print(values)

    if isinstance(values, tuple):
        cursor.execute(insert_stmt, values)

    elif isinstance(values, list):
        cursor.executemany(insert_stmt, values)

def update(cursor, table: str, fields: tuple, values: list[tuple] | tuple, where: str | tuple = ""):
    if not table:
        raise ValueError("No table has been provided.")

    if not isinstance(fields, (tuple, list)) or not fields:
        raise ValueError("Fields must be a non-empty tuple.")

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

    set_stmt = ", ".join([f"{field} = %s" for field in fields])

    update_stmt = f"UPDATE {table} SET {set_stmt}{Statements.get_where(where)}"
    print(update_stmt)

    if isinstance(values, tuple):
        if isinstance(where, tuple) and where:
            cursor.execute(update_stmt, values + where[1])

        else:
            cursor.execute(update_stmt, values)

    elif isinstance(values, list):
        if isinstance(where, tuple) and where:
            cursor.executemany(update_stmt, [val + where[1] for val in values])

        else:
            cursor.executemany(update_stmt, values)

def query_from_string(cursor, query_stmt: str):
    cursor.execute(query_stmt)

    return cursor.fetchall()

def query_from_table(cursor, table: str, selection: str | tuple = "*", where: str | tuple = "", extra: str = ""):
    if not table:
        raise ValueError("No table has been provided.")

    if isinstance(selection, tuple):
        selection: str = ", ".join(selection)
    elif isinstance(selection, str):
        selection: str = selection

    query_stmt: str = f"SELECT {selection} FROM {table}{Statements.get_where(where)}{extra};"

    print(query_stmt)

    cursor.execute(query_stmt)

    return cursor.fetchall()

class Insert:
    @staticmethod
    def from_string(cursor, insert_stmt: str, values: list[tuple] | tuple) -> None:
        if not insert_stmt:
            raise ValueError("No insert statement has been provided.")

        if not isinstance(values, (tuple, list)) or not values:
            raise ValueError("Values must be a non-empty tuple or list.")

        if isinstance(values, tuple):
            cursor.execute(insert_stmt, values)

        elif isinstance(values, list):
            cursor.executemany(insert_stmt, values)