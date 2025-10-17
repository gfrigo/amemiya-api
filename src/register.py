from src.database import Insert, Statements
from src.map import add, edit


def assemble_add(mapping: dict) :

        register_stmt: str = f"INSERT INTO {mapping["table"]} ({', '.join(mapping["fields"])}) VALUES ({', '.join(['%s'] * len(mapping["fields"]))})"

        return len(mapping["fields"]), register_stmt


def assemble_edit(mapping: dict, data: dict, key: str):

    fields = [field for field in mapping["fields"] if field in data and data[field] is not None]

    set_stmt = ", ".join([f"{field} = %s" for field in fields])

    update_stmt = f"UPDATE {mapping['table']} SET {set_stmt}{Statements.get_where(key)};"

    values = tuple(data[field] for field in fields)

    return update_stmt, values

class Register:
    """
        Class to handle registrations to the database based on predefined patterns.
    """

    @staticmethod
    def add(cursor, entity: str, values: tuple) -> None:
        """
            Inserts a record for a given entity.

            Args:
                cursor: Database cursor to execute the insertion.
                entity (*dict*): Type to be looked up on a mapping dictionary, containing data like table, fields...
                values (*tuple*): A tuple containing the values to be inserted into the user table, should contain: \n'("name", "inner_register", "password", "email", "telephone", "role_id", "admin", "company_id", "image_path", "active_user")'

            Raises:
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

        Insert.from_string(cursor, stmt, values)

    @staticmethod
    def edit(cursor, entity: str, data: dict, key: str, values: tuple) -> None:
        """
                    Edits an existing database record for a given entity.

                    Args:
                        cursor: Database cursor to execute the insertion.
                        entity (*dict*): Type to be looked up on a mapping dictionary, containing data like table, fields...
                        values (*tuple*): A tuple containing the values to be inserted into the user table, should contain: \n'("name", "inner_register", "password", "email", "telephone", "role_id", "admin", "company_id", "image_path", "active_user")'

                    Raises:
                        ValueError: If the number of fields and values do not match
                """

        mapping: dict = edit.get(entity)
        if not mapping:
            raise KeyError(f"Unknown entity '{entity}'")

        stmt, values = assemble_edit(mapping, data, key)

        print(stmt)
        print(values)

        Insert.from_string(cursor, stmt, values)

    @staticmethod
    def remove():
        # TODO
        ...

