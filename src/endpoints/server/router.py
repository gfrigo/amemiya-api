from fastapi import APIRouter
from main import logger

router = APIRouter(prefix="/server", tags=["Server"])

@router.get("/status")
def server_status():
    logger.info("SERVER ROUTE HIT")
    """Checks server status."""
    return {"status": "ok"}