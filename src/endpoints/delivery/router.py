from fastapi import APIRouter, UploadFile, File, Form, HTTPException, status
from src.core.logging_config import logger
from .model import DeliveryDataRequest
from .service import fetch_attachment_service, add_route_service, edit_attachment_service, remove_attachment_service
from datetime import datetime

router = APIRouter(prefix="/delivery", tags=["Delivery"])

@router.get("/{delivery_id}", status_code=status.HTTP_200_OK)
def fetch_delivery(
        delivery_id: int,
        vehicle_id: int | None = None,
        route_id: int | None = None,
        finish_time: str | None = None,
        load_name: str | None = None,
        start_time: str | None = None,
    ):
    logger.info("FETCH DELIVERY ROUTE HIT")

    try:
        result = fetch_attachment_service(
            delivery_id,
            vehicle_id,
            route_id,
            finish_time,
            load_name,
            start_time,
            status,
        )

        return {"detail": result}
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/{company_id}", status_code=status.HTTP_201_CREATED)
def add_route(
        company_id: int,
        request: DeliveryDataRequest
        ):
    """Passes the 'add route' request to the service"""
    logger.info("ADD ROUTE ROUTE HIT")

    raw_data = request.model_dump()
    data = {
        "company_id": company_id,
        "user_id": raw_data["user_id"],
        "creation_datetime": str(datetime.now()),
        "subroutes": raw_data["subroutes"]
    }

    try:
        add_route_service(data)
        return {"detail": "Route added successfully"}
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        logger.error(f"Error while adding route: {e}")
        raise HTTPException(status_code=500, detail="Internal server error")

@router.put("/{attachment_id}", status_code=status.HTTP_204_NO_CONTENT)
def edit_attachment(attachment_id: int, request: DeliveryDataRequest):
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