import os
import logging
from fastapi import FastAPI, responses
from pydantic import BaseModel
from dotenv import load_dotenv
from pathlib import Path
from src.database import start_connection, start_cursor
from src.login import get_access, get_user_data
from src.register import Register

logging.basicConfig(level=logging.INFO)
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


class UserDataRequest(BaseModel):
    user_id: int | None = None
    name: str
    inner_register: str
    password: str | None = None
    email: str
    telephone: str
    role_id: int
    admin: bool
    company_id: int
    image_path: str | None = None
    active_user: bool | None = None

@app.post("/user/add")
def add_user(request: UserDataRequest):
    logger.info("ADD USER ROUTE HIT")

    if not request.password:
        return responses.JSONResponse(status_code=400, content={"detail": "Required field 'password' is missing"})

    with start_connection(DB_HOST, DB_USER, DB_PASSWORD, DB_SCHEMA) as conn:
        with start_cursor(conn) as cursor:
            try:
                Register.add(cursor, "user", (
                    request.name,
                    request.inner_register,
                    request.password,
                    request.email,
                    request.telephone,
                    str(request.role_id),
                    request.admin if request.admin else '0',
                    str(request.company_id),
                    request.image_path if request.image_path else 'assets/profiles/default.png',
                    '1'
                ))
                #conn.commit()
                logger.info("User added successfully")
                return responses.JSONResponse(status_code=201, content={"detail": "User added successfully"})
            except Exception as e:
                logger.error(f"Error adding user: {e}")
                return responses.JSONResponse(status_code=400, content={"detail": str(e)})

@app.post("/user/edit")
def edit_user(request: UserDataRequest):
    logger.info("EDIT USER ROUTE HIT")

    if not request.user_id:
        return responses.JSONResponse(status_code=400, content={"detail": "Required field 'user_id' is missing"})

    with start_connection(DB_HOST, DB_USER, DB_PASSWORD, DB_SCHEMA) as conn:
        with start_cursor(conn) as cursor:
            try:
                Register.edit(cursor, "user", request.model_dump(), f"user_id = {request.user_id}", (
                    request.name,
                    request.inner_register,
                    request.password if request.password else '',
                    request.email,
                    request.telephone,
                    str(request.role_id),
                    request.admin if request.admin else '0',
                    str(request.company_id),
                    request.image_path if request.image_path else 'assets/profiles/default.png',
                    request.active_user if request.active_user else '1'
                ))
                conn.commit()
                logger.info("User register edited successfully")
                return responses.JSONResponse(status_code=201, content={"detail": "User register edited successfully"})
            except Exception as e:
                logger.error(f"Error adding user: {e}")
                return responses.JSONResponse(status_code=400, content={"detail": str(e)})