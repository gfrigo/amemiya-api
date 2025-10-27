from fastapi import APIRouter, HTTPException, status
from src.core.logging_config import logger
from .model import AttachmentDataRequest
from .service import fetch_attachment_service, add_user_service, edit_user_service, remove_user_service

router = APIRouter(prefix="/attachment", tags=["Attachment"])

@router.get("/{company_id}", status_code=status.HTTP_200_OK)
def fetch_attachment(
    company_id: int,
    user_id: int | None = None):
    logger.info("FETCH ATTACHMENT ROUTE HIT")
    try:
        result = fetch_attachment_service(company_id, user_id)
        return {"detail": result}
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/{company_id}", status_code=status.HTTP_201_CREATED)
def add_attachment(company_id: int, request: AttachmentDataRequest):
    """Passes the 'add attachment' request to the service"""
    logger.info("ADD ATTACHMENT ROUTE HIT")
    try:
        print(company_id, request)
        #result = add_attachment_service(request)
        #return {"detail": "Attachment added successfully", "data": result}
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
        ...
        #result = edit_attachment_service(attachment_id, request)
        #return {"detail": "Attachment edited successfully", "data": result}
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
        ...
        #result = remove_attachment_service(attachment_id)
        #return {"detail": "Attachment removed successfully", "data": result}
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        logger.error(f"Error while removing attachment: {e}")
        raise HTTPException(status_code=500, detail="Internal server error")