from fastapi import APIRouter, HTTPException
from src.core.logging_config import logger
from .model import UserDataRequest
from .service import fetch_user_service, add_user_service, edit_user_service, remove_user_service

router = APIRouter(prefix="/user", tags=["User"])

@router.post("/fetch")
def fetch_user(request: UserDataRequest):
    logger.info("FETCH USER ROUTE HIT")
    try:
        result = fetch_user_service(request)
        return {"detail": result}
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/add")
def add_user(request: UserDataRequest):
    logger.info("ADD USER ROUTE HIT")
    try:
        result = add_user_service(request)
        return {"detail": result}
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Internal server error {str(e)}")

@router.post("/edit")
def edit_user(request: UserDataRequest):
    logger.info("EDIT USER ROUTE HIT")
    try:
        result = edit_user_service(request)
        return {"detail": result}
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Internal server error {str(e)}")

@router.post("/remove")
def remove_user(request: UserDataRequest):
    logger.info("REMOVE USER ROUTE HIT")
    try:
        result = remove_user_service(request)
        return {"detail": result}
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Internal server error {e}")