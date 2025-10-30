from src.core.logging_config import logger
from src.core.database import Execute, Statements
from src.map import fetch, add, edit, remove
from pypika import Field, Table, Query, Parameter, MySQLQuery


def assemble_fetch(mapping: dict, filter_stmt: str | tuple | None = None) -> str:

    if not filter_stmt:
        where_stmt: str = ""
    else:
        where_stmt: str = Statements.get_where(filter_stmt)

    query_stmt: str = f"SELECT {mapping['selection']} FROM {mapping['table']}{where_stmt};"

    return query_stmt

def assemble_add(mapping: dict) -> tuple:

        register_stmt: str = f"INSERT INTO {mapping['table']} ({', '.join(mapping['fields'])}) VALUES ({', '.join(['%s'] * len(mapping['fields']))})"

        return len(mapping["fields"]), register_stmt

def assemble_edit(mapping: dict, data: dict, key: str | tuple | None) -> tuple:
    logger.info("ASSEMBLYING EDIT STATEMENT")

    table = Table(mapping["table"])
    query = MySQLQuery.update(table)

    fields = [f for f in mapping["fields"] if f in data and data[f] is not None]

    print(fields)

    for f in fields:
        query = query.set(table[f], Parameter('%s'))

    if key:
        if isinstance(key, str):
            field, value = key.split(" = ")
            try:
                value = int(value)
            except ValueError:
                value = value.strip("'\"")
            query = query.where(Field(field) == value)

        elif isinstance(key, tuple):
            for condition in key:
                field, value = condition.split(" = ")
                try:
                    value = int(value)
                except ValueError:
                    value = value.strip(r'\"')
                query = query.where(Field(field) == value)

    query_str = str(query) + ";"
    values = tuple(data[f] for f in fields)

    return query_str, values

def assemble_remove(mapping: dict, key: str) -> str:

    delete_stmt = f"DELETE FROM {mapping['table']}{Statements.get_where(key)};"

    return delete_stmt

class Register:
    """
        Class to handle registrations to the database based on predefined patterns.
    """

    @staticmethod
    def fetch(cursor, entity: str, filter_stmt: str | tuple | None) -> list:
        """
            Queries from the database for a given entity.

            Args:
                cursor: Database cursor to execute the insertion.
                entity (*dict*): Type to be looked up on a mapping dictionary, containing data like table, fields...
                filter_stmt (*str*): Column(s) to be selected from the database.

            Raises:
                KeyError: If the entity is not found in the mapping dictionary.
        """

        mapping: dict = fetch.get(entity)

        if not mapping:
            raise KeyError(f"Unknown entity '{entity}'")

        stmt = assemble_fetch(mapping, filter_stmt)

        print(stmt)

        result: list = Execute.Select.from_string(cursor, stmt)
        return result

    @staticmethod
    def add(cursor, entity: str, values: tuple) -> None:
        """
            Inserts a record for a given entity.

            Args:
                cursor: Database cursor to execute the insertion.
                entity (*dict*): Type to be looked up on a mapping dictionary, containing data like table, fields...
                values (*tuple*): A tuple containing the values to be inserted into the user table, should contain: \n'("name", "inner_register", "password", "email", "telephone", "role_id", "admin", "company_id", "image_path", "active_user")'

            Raises:
                KeyError: If the entity is not found in the mapping dictionary.
                ValueError: If the number of fields and values do not match
        """

        mapping: dict = add.get(entity)
        if not mapping:
            raise KeyError(f"Unknown entity '{entity}'")

        fields_length, stmt = assemble_add(mapping)
        if len(values) != fields_length:
            raise ValueError("Fields and Values have different lengths")
        
        print(stmt)
        print(values)

        Execute.Insert.from_string(cursor, stmt, values)

    @staticmethod
    def edit(cursor, entity: str, data: dict, key: str) -> None:
        """
            Edits an existing database record for a given entity.

            Args:
                cursor: Database cursor to execute the insertion.
                entity (*str*): Type to be looked up on a mapping dictionary, containing data like table, fields...
                data (*dict*): A dictionary containing the fields to be updated and their new values.
                key (*str*): The condition to identify the record to be updated.

            Raises:
                KeyError: If the entity is not found in the mapping dictionary.
        """

        mapping: dict = edit.get(entity)
        if not mapping:
            raise KeyError(f"Unknown entity '{entity}'")

        stmt, values = assemble_edit(mapping, data, key)

        logger.info(f"Update statement: {stmt}")
        logger.info(f"Value: {values}")

        Execute.Update.from_string(cursor, stmt, values)

    @staticmethod
    def remove(cursor, entity: str, key: str):
        """
            Removes an existing database record for a given entity.

            Args:
                cursor: Database cursor to execute the insertion.
                entity (*str*): Type to be looked up on a mapping dictionary, containing data like table, fields...
                key (*str*): The condition to identify the record to be deleted.

            Raises:
                KeyError: If the entity is not found in the mapping dictionary.
        """

        mapping: dict = remove.get(entity)
        if not mapping:
            raise KeyError(f"Unknown entity '{entity}'")

        stmt = assemble_remove(mapping, key)

        print(stmt)

        Execute.Delete.from_string(cursor, stmt)