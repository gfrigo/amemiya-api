from fastapi import APIRouter, UploadFile, File, Form, HTTPException, status
from fastapi.responses import Response, JSONResponse
from src.core.logging_config import logger
from .model import UserDataRequest
from .service import fetch_user_service, add_user_service, edit_user_service, remove_user_service
from src.endpoints.attachment.model import AttachmentDataRequest
from src.endpoints.attachment.service import add_attachment_service
from datetime import datetime

router = APIRouter(prefix="/user", tags=["User"])

@router.post("/fetch")
def fetch_user(request: UserDataRequest):
    logger.info("FETCH USER ROUTE HIT")
    try:
        result = fetch_user_service(request)

        if result:
            return JSONResponse(status_code=status.HTTP_200_OK, content=result)

        return Response(status_code=status.HTTP_204_NO_CONTENT)

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

@router.put("/profile_picture/{user_id}", status_code=status.HTTP_201_CREATED)
async def edit_user(user_id: int, company_id: int = Form(...), file_type: str = Form(...), file: UploadFile = File(...)):
    logger.info("ADD USER PROFILE PICTURE ROUTE HIT")

    file_bytes: bytes = await file.read()

    attachment_data = AttachmentDataRequest(
        uploaded_by_company_id=company_id,
        uploaded_by_user_id=user_id,
        file_data=file_bytes,
        file_type=file_type,
        attachment_type="profile_picture",
        upload_date = str(datetime.now())
    )

    try:
        attachment_id = add_attachment_service(attachment_data)

        user_data = {
            "user_id": user_id,
            "profile_picture_id": attachment_id
        }

        result = edit_user_service(user_data)

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