import os
from src.core.utils import get_hash
from dotenv import load_dotenv
from pathlib import Path
from src.core.database import start_connection, start_cursor, Statements
from src.register import Register

env_path: Path = Path(".env")
load_dotenv(env_path)

DB_HOST: str = os.getenv("DB_HOST")
DB_USER: str = os.getenv("DB_USER")
DB_PASSWORD: str = os.getenv("DB_PASSWORD")
DB_SCHEMA: str | None = os.getenv("DB_SCHEMA")

with start_connection(DB_HOST, DB_USER, DB_PASSWORD, DB_SCHEMA) as conn:
    with start_cursor(conn) as cursor:

        with open("test.pdf", "rb") as file:
            binary_data = file.read()

        cursor.execute("INSERT INTO Attachment (attachment_data, attachment_type) VALUES (%s, %s);", (binary_data, "pdf"))

        conn.commit()