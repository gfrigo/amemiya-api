from fastapi import APIRouter, UploadFile, File, Form, HTTPException, status
from fastapi.responses import Response, JSONResponse
from src.core.logging_config import logger
from .model import AttachmentDataRequest
from .service import fetch_attachment_service, add_attachment_service, edit_attachment_service, remove_attachment_service
from datetime import datetime

router = APIRouter(prefix="/attachment", tags=["Attachment"])

@router.get("/{company_id}", status_code=status.HTTP_200_OK)
def fetch_attachment(
        company_id: int,
        user_id: int | None = None,
        attachment_type: str | None = None,
        date_range_start: str | None = None,
        date_range_end: str | None = None
    ):
    logger.info("FETCH ATTACHMENT ROUTE HIT")

    try:
        attachment_data = fetch_attachment_service(
            company_id,
            user_id,
            attachment_type,
            date_range_start,
            date_range_end
        )

        if attachment_data:
            return JSONResponse(status_code=status.HTTP_200_OK, content={"data": attachment_data})

        return Response(status_code=status.HTTP_204_NO_CONTENT)

    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/{company_id}", status_code=status.HTTP_201_CREATED)
async def add_attachment(
        company_id: int,
        user_id: int = Form(...),
        file: UploadFile = File(...),
        file_type: str = Form(...),
        attachment_type: str = Form(...)
        ):
    """Passes the 'add attachment' request to the service"""
    logger.info("ADD ATTACHMENT ROUTE HIT")

    file_bytes: bytes = await file.read()

    request_data = AttachmentDataRequest(
        uploaded_by_company_id=company_id,
        uploaded_by_user_id=user_id,
        file_data=file_bytes,
        file_type=file_type,
        attachment_type=attachment_type,
        upload_date=str(datetime.now())
    ).model_dump()

    try:
        add_attachment_service(request_data)

        return Response(status_code=status.HTTP_204_NO_CONTENT)

    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        logger.error(f"Error while adding attachment: {e}")
        raise HTTPException(status_code=500, detail="Internal server error")

@router.put("/{attachment_id}")
def edit_attachment(attachment_id: int, request: AttachmentDataRequest):
    """Passes the 'edit attachment' request to the service"""
    logger.info(f"EDIT ATTACHMENT ROUTE HIT: {attachment_id}")

    request_data = request.model_dump()
    request_data["attachment_id"] = attachment_id

    try:
        edit_attachment_service(request_data)
        return Response(status_code=status.HTTP_204_NO_CONTENT)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        logger.error(f"Error while editing attachment: {e}")
        raise HTTPException(status_code=500, detail="Internal server error")

@router.delete("/{attachment_id}", status_code=status.HTTP_204_NO_CONTENT)
def remove_attachment(attachment_id: int):
    """Passes the 'remove attachment' request to the service"""
    logger.info("REMOVE ATTACHMENT ROUTE HIT")
    try:
        remove_attachment_service(attachment_id)
        return {"detail": "Attachment removed successfully"}
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        logger.error(f"Error while removing attachment: {e}")
        raise HTTPException(status_code=500, detail="Internal server error")