from src.database import Statements

fetch: dict = {
    "user": {
        "table": "Users",
        "selection": "*",
        "filter": {
            "activeUser": ("activeUser = 1", )
        }
    },
    "vehicle": {
        "table"
    }
}

def assemble_fetch(type_fetch: str, query_filter: str = "", fetch_map: dict = None):
    if fetch_map is None:
        fetch_map = fetch

    type_map: dict = fetch_map[type_fetch]

    if not query_filter:
        where_stmt: str = ""
    else:
        where_stmt: str = Statements.get_where(type_map["filter"][query_filter])

    query_stmt: str = f"SELECT {type_map["selection"]} FROM {type_map["table"]}{where_stmt};"

    print(query_stmt)

register: dict = {
    "user": {
        "table": "Users",
        "fields": ("name", "innerRegister", "password", "email", "telephone", "roleId", "admin", "companyId", "imagePath", "activeUser")
    },
    "vehicle": {
        "table": ""
    }
}

def assemble_register(type_register: str, values: tuple = None, register_map: dict = None):
    if register_map is None:
        register_map = register

    type_map: dict = register_map[type_register]

    register_stmt: str = f"INSERT INTO {type_map["table"]} {type_map["fields"]}"

    print(register_stmt)

assemble_register("user")

