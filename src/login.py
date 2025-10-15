from pathlib import Path
import os
from dotenv import load_dotenv
import logging
from src.lib import get_hash
from src.database import start_connection, start_cursor, query_from_table

env_path: Path = Path(".env")
load_dotenv(env_path)

DB_HOST: str =os.getenv("DB_HOST")
DB_USER: str = os.getenv("DB_USER")
DB_PASSWORD: str = os.getenv("DB_PASSWORD")
DB_SCHEMA: str | None = os.getenv("DB_SCHEMA")

def query_users() -> list[tuple] | None:
    with start_connection(DB_HOST, DB_USER, DB_PASSWORD, DB_SCHEMA) as conn:
        with start_cursor(conn) as cursor:
            users = query_from_table(cursor, "Users", "*")
            return users
        
def get_login_access(user:str, password: str) -> bool:
    usersData = query_users()

    for userData in usersData:
        if userData[1] == user and userData[3] == get_hash(password):
            return True
        
    return False
