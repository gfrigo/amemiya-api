import logging
from fastapi import FastAPI
from src.endpoints.server.router import router as server_router
from src.endpoints.user.router import router as user_router
from src.endpoints.login.router import router as login_router

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("uvicorn")

app = FastAPI()

app.include_router(server_router)
app.include_router(user_router)
app.include_router(login_router)

