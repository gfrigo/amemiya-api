from src.lib import get_hash
from src.queries import User
from src.database import query_from_table, query_from_string

def query_users(cursor, only_active: bool = False) -> list[tuple] | None:
    if only_active:
        users = query_from_table(cursor, "Users", "*", "active_user = 1")
    else:
        users = query_from_table(cursor, "Users", "*")
    return users
        
def get_access(cursor, user:str, password: str) -> dict:
    users_data = query_users(cursor, only_active=True)

    for user_entry in users_data:
        if user_entry[1] == user and user_entry[3] == get_hash(password):
            return {"access": True, "user_id": user_entry[0]}
        
    return {"access": False, "user_id": None}

def get_user_data(cursor, access_data: dict) -> tuple:
    if access_data["access"]:
        user_data = query_from_string(cursor, User.get_data(access_data["user_id"]))[0]

        return (True, {
            "name": user_data[0],
            "inner_register": user_data[1],
            "email": user_data[2],
            "telephone": user_data[3],
            "role": user_data[4],
            "admin": user_data[5],
            "company": user_data[6],
            "image_path": user_data[7]
        })

    return (False, )
