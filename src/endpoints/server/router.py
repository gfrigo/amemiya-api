from fastapi import APIRouter
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("uvicorn")

router = APIRouter(prefix="/server", tags=["Server"])

@router.get("/status")
def server_status():
    """Checks server status."""
    return {"status": "ok"}