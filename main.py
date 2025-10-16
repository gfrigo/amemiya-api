import os
import logging
from fastapi import FastAPI, responses
from pydantic import BaseModel
from dotenv import load_dotenv
from pathlib import Path
from src.database import start_connection, start_cursor
from src.login import get_access, get_user_data

logger = logging.getLogger("uvicorn")

env_path: Path = Path(".env")
load_dotenv(env_path)

DB_HOST: str = os.getenv("DB_HOST")
DB_USER: str = os.getenv("DB_USER")
DB_PASSWORD: str = os.getenv("DB_PASSWORD")
DB_SCHEMA: str | None = os.getenv("DB_SCHEMA")

app = FastAPI()

class LoginRequest(BaseModel):
    user: str
    password: str

@app.post("/login")
def login(request: LoginRequest):
    logger.info("LOGIN ROUTE HIT")
    with start_connection(DB_HOST, DB_USER, DB_PASSWORD, DB_SCHEMA) as conn:
        with start_cursor(conn) as cursor:

            access = get_access(cursor, request.user, request.password)
            logger.info(f"ACCESS: {access}")

            user_data = get_user_data(cursor, access)
            logger.info(f"USER DATA: {user_data}")

            if user_data[0]:
                return responses.JSONResponse(status_code=200, content={"detail": user_data[1]})

            else:
                return responses.JSONResponse(status_code=401, content={"detail": "Unauthorized"})


