import os
from src.lib import get_hash
from dotenv import load_dotenv
from pathlib import Path
from src.database import start_connection, start_cursor
from src.register import Register

env_path: Path = Path(".env")
load_dotenv(env_path)

DB_HOST: str = os.getenv("DB_HOST")
DB_USER: str = os.getenv("DB_USER")
DB_PASSWORD: str = os.getenv("DB_PASSWORD")
DB_SCHEMA: str | None = os.getenv("DB_SCHEMA")


with start_connection(DB_HOST, DB_USER, DB_PASSWORD, DB_SCHEMA) as conn:
    with start_cursor(conn) as cursor:
        Register.add(cursor, ("TesteRegistro", "TR123", get_hash("senha123"), "teste2@example.com", "1234567890", "1", "0", "1", None, "1"))

        conn.commit()