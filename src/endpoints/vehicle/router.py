from fastapi import APIRouter, HTTPException, status
from fastapi.responses import JSONResponse, Response

from src.core.config import logger
from .model import VehicleDataRequest
from .service import fetch_vehicle_service, add_vehicle_service, edit_vehicle_service, remove_vehicle_service

router = APIRouter(prefix="/vehicle", tags=["Vehicle"])

@router.get("/{company_id}")
def fetch_vehicle(
        company_id: int,
        vehicle_id: int | None = None,
        vehicle_name: str | None = None,
        license_plate: str | None = None,
        brand: str | None = None,
        model: str | None = None,
        year: int | None = None,
        date_range_start: str | None = None,
        date_range_end: str | None = None,
        last_user_id: int | None = None,
        active_vehicle: bool = True
):
    logger.info("FETCH VEHICLE ROUTE HIT")

    request_data = {
        "company_id": company_id,
        "vehicle_id": vehicle_id,
        "vehicle_name": vehicle_name,
        "license_plate": license_plate,
        "brand": brand,
        "model": model,
        "year": year,
        "date_range_start": date_range_start,
        "date_range_end": date_range_end,
        "last_user_id": last_user_id,
        "active_vehicle": active_vehicle
    }

    try:
        vehicle_data = fetch_vehicle_service(request_data)

        if vehicle_data:
            return JSONResponse(status_code=status.HTTP_200_OK, content={"data": vehicle_data})

        return Response(status_code=status.HTTP_204_NO_CONTENT)

    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/{company_id}")
def add_vehicle(
        company_id: int,
        request: VehicleDataRequest
):
    logger.info("ADD VEHICLE ROUTE HIT")

    request_data = request.model_dump()
    request_data["company_id"] = company_id

    try:
        vehicle_id: int = add_vehicle_service(request_data)

        if not vehicle_id:
            return Response(status_code=status.HTTP_400_BAD_REQUEST)

        return JSONResponse(status_code=status.HTTP_201_CREATED, content={"vehicle_id": vehicle_id})

    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Internal server error {str(e)}")

@router.put("/{vehicle_id}")
def edit_vehicle(
        vehicle_id: int,
        request: VehicleDataRequest
):
    logger.info("EDIT VEHICLE ROUTE HIT")

    request_data = request.model_dump()
    request_data["vehicle_id"] = vehicle_id

    try:
        edit_vehicle_service(request_data)

        return Response(status_code=status.HTTP_204_NO_CONTENT)

    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Internal server error {str(e)}")

@router.delete("/{vehicle_id}")
def remove_vehicle(vehicle_id: int):
    logger.info("REMOVE VEHICLE ROUTE HIT")

    request_data = {"vehicle_id": vehicle_id}

    try:
        remove_vehicle_service(request_data)

        return Response(status_code=status.HTTP_204_NO_CONTENT)

    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Internal server error {e}")