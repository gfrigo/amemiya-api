import os
from src.lib import get_hash
from dotenv import load_dotenv
from pathlib import Path
from src.database import start_connection, start_cursor, Statements
from src.register import Register

env_path: Path = Path(".env")
load_dotenv(env_path)

DB_HOST: str = os.getenv("DB_HOST")
DB_USER: str = os.getenv("DB_USER")
DB_PASSWORD: str = os.getenv("DB_PASSWORD")
DB_SCHEMA: str | None = os.getenv("DB_SCHEMA")

print(Statements.get_where("user_id = 1"))

"""with start_connection(DB_HOST, DB_USER, DB_PASSWORD, DB_SCHEMA) as conn:
    with start_cursor(conn) as cursor:
        Register.add(cursor, "user", ("TesteRegistro", "TR123", get_hash("senha123"), "teste3@example.com", "2345678901", "1", "0", "1"))

        conn.commit()"""