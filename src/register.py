from src.database import Insert
from src.map import register

def assemble_register(mapping: dict) :

        register_stmt: str = f"INSERT INTO {mapping["table"]} ({', '.join(mapping["fields"])}) VALUES ({', '.join(['%s'] * len(mapping["fields"]))})"

        return len(mapping["fields"]), register_stmt

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
                values (*tuple*): A tuple containing the values to be inserted into the user table, should contain: \n'("name", "innerRegister", "password", "email", "telephone", "roleId", "admin", "companyId", "imagePath", "activeUser")'

            Raises:
                ValueError: If the number of fields and values do not match
        """

        mapping: dict = register.get(entity)
        if not mapping:
            raise KeyError(f"Unknown entity '{entity}'")

        fields_length, stmt = assemble_register(mapping)
        if len(values) != fields_length:
            raise ValueError("Fields and Values have different lengths")
        
        print(stmt)
        print(values)

        Insert.from_string(cursor, stmt, values)

    @staticmethod
    def change():
        # TODO
        ...

    @staticmethod
    def remove():
        # TODO
        ...

