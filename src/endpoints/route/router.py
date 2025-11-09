from fastapi import APIRouter, UploadFile, File, Form, HTTPException, status
from fastapi.responses import Response, JSONResponse
from src.core.logging_config import logger
from .model import RouteDataRequest
from .service import fetch_route_service, add_route_service, edit_route_service, remove_route_service
from datetime import datetime

router = APIRouter(prefix="/route", tags=["Route"])

@router.get("/{company_id}", status_code=status.HTTP_200_OK)
def fetch_route(
        company_id: int,
        route_id: int | None = None,
        user_id: int | None = None,
        country: str | None = None,
        state: str | None = None,
        city: str | None = None,
        district: str | None = None,
        date_range_start: str | None = None,
        date_range_end: str | None = None
    ):
    logger.info("FETCH ROUTE ROUTE HIT")

    request_data = {
        "company_id": company_id,
        "route_id": route_id,
        "user_id": user_id,
        "country": country,
        "state": state,
        "city": city,
        "district": district,
        "date_range_start": date_range_start,
        "date_range_end": date_range_end
    }

    try:
        route_data = fetch_route_service(request_data)

        if route_data:
            return JSONResponse(status_code=status.HTTP_200_OK, content={"data": route_data})

        return Response(status_code=status.HTTP_204_NO_CONTENT)

    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/{company_id}", status_code=status.HTTP_201_CREATED)
def add_route(
        company_id: int,
        request: RouteDataRequest
        ):
    """Passes the 'add route' request to the service"""
    logger.info("ADD ROUTE ROUTE HIT")

    raw_request_data = request.model_dump()
    request_data = {
        "company_id": company_id,
        "user_id": raw_request_data["created_by_user_id"],
        "creation_datetime": str(datetime.now()),
        "subroutes": raw_request_data["subroutes"]
    }

    try:
        add_route_service(request_data)
        return {"detail": "Route added successfully"}
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        logger.error(f"Error while adding route: {e}")
        raise HTTPException(status_code=500, detail="Internal server error")

@router.put("/{route_id}")
def edit_route(route_id: int, request: RouteDataRequest):
    """Passes the 'edit route' request to the service"""
    logger.info(f"EDIT ROUTE ROUTE HIT: {route_id}")

    request_data = request.model_dump()
    request_data["route_id"] = route_id

    try:
        edit_route_service(request_data)
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
        remove_route_service(route_id)
        return Response(status_code=status.HTTP_204_NO_CONTENT)

    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))

    except Exception as e:
        logger.error(f"Error while removing route: {e}")
        raise HTTPException(status_code=500, detail="Internal server error")