from fastapi import APIRouter, HTTPException
from .model import LoginDataRequest
from .service import fetch_login_service
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("uvicorn")

router = APIRouter(prefix="/login", tags=["Login"])

@router.post("/")
def fetch_user(request: LoginDataRequest):
    """Authenticate and return login data."""
    logger.info("LOGIN ROUTE HIT")
    try:
        result = fetch_login_service(request)
        return {"detail": result}
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Internal server error {e}")
