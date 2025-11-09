from fastapi import APIRouter, UploadFile, File, Form, HTTPException, status
from fastapi.responses import Response, JSONResponse
from src.core.logging_config import logger
from .model import GeopointDataRequest
from .service import fetch_geopoint_service, add_geopoint_service, edit_geopoint_service, remove_geopoint_service
from datetime import datetime

router = APIRouter(prefix="/geopoint", tags=["Geopoint"])

@router.get("/{company_id}")
def fetch_geopoint(
        company_id: int,
    ):
    logger.info("FETCH GEOPOINT ROUTE HIT")

    request_data = {
        "company_id": company_id
    }

    try:
        geopoints = fetch_geopoint_service(request_data)

        return JSONResponse(status_code=status.HTTP_200_OK, content=geopoints)

    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/{company_id}")
def add_geopoint(
        company_id: int,
        request: GeopointDataRequest
):
    """Passes the 'add geopoint' request to the service"""
    logger.info("ADD GEOPOINT ROUTE HIT")

    request_data = request.model_dump()
    request_data["company_id"] = company_id

    try:
        geopoint_id: int = add_geopoint_service(request_data)
        return JSONResponse(status_code=status.HTTP_201_CREATED, content={"geopoint_id": geopoint_id})

    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))

    except Exception as e:
        logger.error(f"Error while adding geopoint: {e}")
        raise HTTPException(status_code=500, detail="Internal server error")

@router.put("/{geopoint_id}")
def edit_route(geopoint_id: int, request: GeopointDataRequest):
    """Passes the 'edit route' request to the service"""
    logger.info(f"EDIT GEOPOINT ROUTE HIT: {geopoint_id}")

    request_data = request.model_dump()
    request_data["geopoint_id"] = geopoint_id

    try:
        edit_geopoint_service(request_data)
        return Response(status_code=status.HTTP_204_NO_CONTENT)

    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))

    except Exception as e:
        logger.error(f"Error while editing route: {e}")
        raise HTTPException(status_code=500, detail="Internal server error")

@router.delete("/{route_id}")
def remove_route(route_id: int):
    """Passes the 'remove route' request to the service"""
    logger.info("REMOVE ROUTE ROUTE HIT")
    try:
        remove_geopoint_service(route_id)
        return Response(status_code=status.HTTP_204_NO_CONTENT)

    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))

    except Exception as e:
        logger.error(f"Error while removing route: {e}")
        raise HTTPException(status_code=500, detail="Internal server error")