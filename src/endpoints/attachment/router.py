from fastapi import APIRouter, UploadFile, File, Form, HTTPException, status
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
        result = fetch_attachment_service(
            company_id,
            user_id,
            attachment_type,
            date_range_start,
            date_range_end
        )

        return {"detail": result}
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/", status_code=status.HTTP_201_CREATED)
async def add_attachment(
        company_id: int = Form(...),
        user_id: int = Form(...),
        file: UploadFile = File(...),
        file_type: str = Form(...),
        attachment_type: str = Form(...)
        ):
    """Passes the 'add attachment' request to the service"""
    logger.info("ADD ATTACHMENT ROUTE HIT")

    file_bytes: bytes = await file.read()

    data = AttachmentDataRequest(
        uploaded_by_company_id=company_id,
        uploaded_by_user_id=user_id,
        file_data=file_bytes,
        file_type=file_type,
        attachment_type=attachment_type,
        upload_date=str(datetime.now())
    )

    try:
        add_attachment_service(data)
        return {"detail": "Attachment added successfully"}
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        logger.error(f"Error while adding attachment: {e}")
        raise HTTPException(status_code=500, detail="Internal server error")

@router.put("/{attachment_id}", status_code=status.HTTP_204_NO_CONTENT)
def edit_attachment(attachment_id: int, request: AttachmentDataRequest):
    """Passes the 'edit attachment' request to the service"""
    logger.info(f"EDIT ATTACHMENT ROUTE HIT: {attachment_id}")
    try:
        edit_attachment_service(attachment_id, request)
        return {"detail": "Attachment edited successfully"}
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