from fastapi import FastAPI
from src.core.logging_config import logger
from src.endpoints.server.router import router as server_router
from src.endpoints.login.router import router as login_router
from src.endpoints.user.router import router as user_router
from src.endpoints.vehicle.router import router as vehicle_router
from src.endpoints.attachment.router import router as attachment_router
from src.endpoints.route.router import router as route_router



app = FastAPI()

app.include_router(server_router)
app.include_router(login_router)
app.include_router(user_router)
app.include_router(vehicle_router)
app.include_router(attachment_router)
app.include_router(route_router)
