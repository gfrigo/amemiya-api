import os
from dotenv import load_dotenv
from pathlib import Path
from src.database import start_connection, start_cursor, insert

env_path: Path = Path(".env")
load_dotenv(env_path)

DB_HOST: str =os.getenv("DB_HOST")
DB_USER: str = os.getenv("DB_USER")
DB_PASSWORD: str = os.getenv("DB_PASSWORD")
DB_SCHEMA: str | None = os.getenv("DB_SCHEMA")


with start_connection(DB_HOST, DB_USER, DB_PASSWORD, DB_SCHEMA) as conn:
    with start_cursor(conn) as cursor:
        #cursor.execute("SELECT * from test;")

        insert(cursor, "test", ("name",), [("Gabriel3",), ("Fernando3",), ("Fernando4",)])
        conn.commit()

        #rows = cursor.fetchall()
        #for row in rows:
            #print(row)
