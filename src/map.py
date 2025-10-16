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

def assemble_fetch(type_fetch: str, mapping: dict, query_filter: str = ""):
    type_map: dict = mapping[type_fetch]

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


