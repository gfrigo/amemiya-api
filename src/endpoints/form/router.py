from datetime import datetime

from fastapi import APIRouter, UploadFile, File, Form, HTTPException, status
from fastapi.responses import Response, JSONResponse

from src.core.config import logger
from src.endpoints.attachment.model import AttachmentDataRequest
from src.endpoints.attachment.service import add_attachment_service
from .model import FormDataRequest
from .service import fetch_user_service, add_user_service, edit_user_service, remove_user_service

router = APIRouter(prefix="/user", tags=["User"])

@router.get("/{company_id}")
def fetch_user(
        company_id: int,
        user_id: int | None = None
    ):
    logger.info("FETCH USER ROUTE HIT")

    request_data = {
        "company_id": company_id,
        "user_id": user_id
    }

    try:
        user_data = fetch_user_service(request_data)

        if user_data:
            return JSONResponse(status_code=status.HTTP_200_OK, content={"data": user_data})

        return Response(status_code=status.HTTP_204_NO_CONTENT)

    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/{company_id}")
def add_user(
        company_id: int,
        request: FormDataRequest
    ):
    logger.info("ADD USER ROUTE HIT")

    request_data = request.model_dump()
    request_data["company_id"] = company_id

    try:
        user_id: int = add_user_service(request_data)

        if not user_id:
            return Response(status_code=status.HTTP_400_BAD_REQUEST)

        return JSONResponse(status_code=status.HTTP_201_CREATED, content={"user_id": user_id})

    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Internal server error {str(e)}")

@router.put("/{user_id}")
def edit_user(
        user_id: int,
        request: FormDataRequest
    ):
    logger.info("EDIT USER ROUTE HIT")

    request_data = request.model_dump()
    request_data["user_id"] = user_id

    try:
        edit_user_service(request_data)

        return Response(status_code=status.HTTP_204_NO_CONTENT)

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
    ).model_dump()

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

@router.delete("/{user_id}")
def remove_user(user_id: int):
    logger.info("REMOVE USER ROUTE HIT")

    request_data = {"user_id": user_id}

    try:
        remove_user_service(request_data)

        return Response(status_code=status.HTTP_204_NO_CONTENT)

    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Internal server error {e}")