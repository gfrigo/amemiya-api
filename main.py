import os
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from src.lib import get_hash
from dotenv import load_dotenv
from pathlib import Path
from src.database import start_connection, start_cursor, insert, query_from_table
from src.login import get_login_access

env_path: Path = Path(".env")
load_dotenv(env_path)

app = FastAPI()

class LoginRequest(BaseModel):
    user: str
    password: str

@app.post("/login")
def login(request: LoginRequest):
    access_granted = get_login_access(request.user, request.password)
    if access_granted:
        return {"detail": {"access": True}}
    else:
        raise HTTPException(status_code=401, detail={"access": False})
