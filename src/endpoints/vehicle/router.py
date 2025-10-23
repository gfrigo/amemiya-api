from fastapi import APIRouter, HTTPException
from src.core.logging_config import logger
from .schema import VehicleDataRequest
from .service import fetch_vehicle_service, add_vehicle_service, edit_vehicle_service, remove_vehicle_service

router = APIRouter(prefix="/vehicle", tags=["Vehicle"])

@router.post("/fetch")
def fetch_vehicle(request: VehicleDataRequest):
    logger.info("FETCH VEHICLE ROUTE HIT")
    try:
        result = fetch_vehicle_service(request)
        return {"detail": result}
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/add")
def add_vehicle(request: VehicleDataRequest):
    logger.info("ADD VEHICLE ROUTE HIT")
    try:
        result = add_vehicle_service(request)
        return {"detail": result}
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Internal server error {str(e)}")

@router.post("/edit")
def edit_vehicle(request: VehicleDataRequest):
    logger.info("EDIT VEHICLE ROUTE HIT")
    try:
        result = edit_vehicle_service(request)
        return {"detail": result}
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Internal server error {str(e)}")

@router.post("/remove")
def remove_vehicle(request: VehicleDataRequest):
    logger.info("REMOVE VEHICLE ROUTE HIT")
    try:
        result = remove_vehicle_service(request)
        return {"detail": result}
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Internal server error {e}")