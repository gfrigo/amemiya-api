from fastapi import APIRouter, HTTPException, status
from fastapi.responses import Response
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
        if not result[0] or not result[1]:
            return Response(status_code=status.HTTP_204_NO_CONTENT)
        return {"detail": {"access": result[0], "data": result[1]}}
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Internal server error {e}")
