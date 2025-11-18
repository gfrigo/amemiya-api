from fastapi import APIRouter, HTTPException, status
from fastapi.responses import Response, JSONResponse

from src.core.config import logger
from .model import LoginDataRequest
from .service import fetch_login_service

router = APIRouter(prefix="/login", tags=["Login"])

@router.post("/")
def fetch_user(request: LoginDataRequest):
    """Authenticate and return login data."""
    logger.info("LOGIN ROUTE HIT")

    raw_data = request.model_dump()
    data = {
        "email": raw_data["email"],
        "password": raw_data["password"]
    }

    try:
        access, user_data, token = fetch_login_service(data)

        if not access or not user_data:
            return Response(status_code=status.HTTP_204_NO_CONTENT)

        return JSONResponse(status_code=status.HTTP_200_OK, content={"access": access, "data": user_data, "token": token})

    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Internal server error {e}")