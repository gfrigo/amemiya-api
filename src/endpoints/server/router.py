from datetime import datetime
from fastapi import APIRouter, status
from fastapi.responses import JSONResponse

from main import logger

router = APIRouter(prefix="/server", tags=["Server"])

@router.get("/status")
def server_status():
    logger.info("SERVER ROUTE HIT")
    """Checks server status."""
    return JSONResponse(
        status_code=status.HTTP_200_OK,
        content={
            "server_status": "OK",
            "server_time": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        }
    )
