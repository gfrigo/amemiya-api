from fastapi import APIRouter, UploadFile, File, Form, HTTPException, status, Path, Query
from fastapi.responses import Response, JSONResponse
from src.core.logging_config import logger
from .model import MaintenanceDataRequest
from src.endpoints.attachment.model import AttachmentDataRequest
from .service import fetch_maintenance_service, add_maintenance_service, edit_maintenance_service, remove_maintenance_service
from src.endpoints.attachment.service import add_attachment_service
from datetime import datetime

router = APIRouter(prefix="/maintenance", tags=["Maintenance"])


@router.get(
    "/{company_id}",
    status_code=status.HTTP_200_OK,
    summary="Fetch maintenances for a company",
    description=(
        "Retrieves all maintenances associated with a specific company and found within the filter. "
        "Each maintenances contains location details such as associated vehicle, origin and date."
    ),
    responses={
        200: {
            "description": "List of Maintenances successfully retrieved",
            "content": {
                "application/json": {
                    "data": [
                        {
                          "maintenance_id": 1,
                          "company_id": 1,
                          "company_name": "root",
                          "user_id": 1,
                          "user_name": "Felipe Almeida de Carvalho",
                          "vehicle_id": 2,
                          "vehicle_name": "Veículo Teste",
                          "license_plate": "12a345c",
                          "brand": "Teste",
                          "model": "Modelo Teste",
                          "year": 2025,
                          "attachment_id": 40,
                          "file_data": "...",
                          "file_type": "pdf",
                          "upload_date": "2025-11-10 19:57:39",
                          "maintenance_type": "teste",
                          "maintenance_origin": "Mercado Car",
                          "maintenance_responsible": "João Francisco",
                          "cost": 399.99,
                          "maintenance_date": "2025-11-08"
                        },
                        {
                          "maintenance_id": 2,
                          "company_id": 1,
                          "company_name": "root",
                          "user_id": 1,
                          "user_name": "Felipe Almeida de Carvalho",
                          "vehicle_id": 2,
                          "vehicle_name": "Veículo Teste",
                          "license_plate": "12a345c",
                          "brand": "Teste",
                          "model": "Modelo Teste",
                          "year": 2025,
                          "attachment_id": 41,
                          "file_data": "...",
                          "file_type": "pdf",
                          "upload_date": "2025-11-10 20:40:42",
                          "maintenance_type": "teste",
                          "maintenance_origin": "Mercado Car",
                          "maintenance_responsible": "João Carlos",
                          "cost": 199.99,
                          "maintenance_date": "2025-05-12"
                        }
                      ]
                }
            },
        },
        400: {"description": "Invalid company ID or bad request"},
        404: {"description": "No maintenances found for the given company"},
        500: {"description": "Internal server error"},
    },
)
def fetch_maintenance(
    company_id: int = Path(..., description="Unique ID of the company whose maintenances should be retrieved", gt=0),
    user_id: int | None = Query(None, description="Unique ID of the user whose maintenances are associated to", gt=0),
    vehicle_id: int | None = Query(None, description="Unique ID of the vehicle whose maintenances are associated to", gt=0),
    cost_range_lower: float | None = Query(None, description="Minimum cost to filter maintenances by", gt=0),
    cost_range_higher: float | None = Query(None, description="Maximum cost to filter maintenances by", gt=0),
    maintenance_type: str | None = Query(None, description="Specific maintenance type to search for"),
    maintenance_origin: str | None = Query(None, description="Issuer or origin of the maintenance"),
    maintenance_responsible: str | None = Query(None, description="Issuer or responsible for the maintenance"),
    maintenance_date_range_start: str | None = Query(None, description="Start of the date range to filter maintenance date by"),
    maintenance_date_range_end: str | None = Query(None, description="End of the date range to filter maintenance date by"),
):
    logger.info("FETCH MAINTENANCE ROUTE HIT")

    request_data = {
        "company_id": company_id,
        "user_id": user_id,
        "vehicle_id": vehicle_id,
        "cost_range_lower": cost_range_lower,
        "cost_range_higher": cost_range_higher,
        "maintenance_type": maintenance_type,
        "maintenance_origin": maintenance_origin,
        "maintenance_responsible": maintenance_responsible,
        "maintenance_date_range_start": maintenance_date_range_start,
        "maintenance_date_range_end": maintenance_date_range_end
    }

    try:
        maintenances_data: list = fetch_maintenance_service(request_data)

        return JSONResponse(status_code=status.HTTP_200_OK, content={"data": maintenances_data})

    except ValueError as e:
        return Response(status_code=status.HTTP_400_BAD_REQUEST, content=str(e))

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.post(
    "/{company_id}",
    status_code=status.HTTP_201_CREATED,
    summary="Add a new maintenance",
    description=(
        "Creates a new maintenance record associated with a given company. "
        "The maintenance includes details such as associated vehicle, origin and date. "
        "Returns the ID of the newly created maintenance upon success."
    ),
    responses={
        201: {
            "description": "Maintenance successfully created",
            "content": {
                "application/json": {
                    "maintenance_id": 1
                }
            },
        },
        400: {"description": "Invalid input data"},
        404: {"description": "Company not found"},
        500: {"description": "Internal server error"},
    },
)
async def add_maintenance(
        company_id: int = Path(...),
        user_id: int = Form(...),
        vehicle_id: int = Form(...),
        file: UploadFile = File(...),
        file_type: str = Form(...),
        maintenance_type: str = Form(...),
        maintenance_origin: str = Form(...),
        maintenance_responsible: str = Form(...),
        cost: float = Form(...),
        maintenance_date: str = Form(...)
):
    """Passes the 'add maintenance' request to the service"""
    logger.info("ADD MAINTENANCE ROUTE HIT")

    file_bytes: bytes = await file.read()

    attachment_data_request = AttachmentDataRequest(
        uploaded_by_company_id=company_id,
        uploaded_by_user_id=user_id,
        file_data=file_bytes,
        file_type=file_type,
        attachment_type="maintenance",
        upload_date=str(datetime.now())
    ).model_dump()

    try:
        attachment_id: int = add_attachment_service(attachment_data_request)
        if not attachment_id:
            return Response(status_code=status.HTTP_400_BAD_REQUEST)

        maintenance_data_request = MaintenanceDataRequest(
            company_id=company_id,
            user_id=user_id,
            vehicle_id=vehicle_id,
            attachment_id=attachment_id,
            maintenance_type=maintenance_type,
            maintenance_origin=maintenance_origin,
            maintenance_responsible=maintenance_responsible,
            cost=cost,
            maintenance_date=maintenance_date
        ).model_dump()

        maintenance_id: int = add_maintenance_service(maintenance_data_request)

        return JSONResponse(status_code=status.HTTP_201_CREATED, content={"maintenance_id": maintenance_id})

    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))

    except Exception as e:
        logger.error(f"Error while adding maintenance: {e}")
        raise HTTPException(status_code=500, detail="Internal server error")

@router.put(
"/{maintenance_id}",
    status_code=status.HTTP_204_NO_CONTENT,
    summary="Edit a maintenance",
    description=(
        "Updates an existing maintenance record in the database. "
        "All fields provided in the request body will replace the existing values. "
        "If a field is omitted or set to `null`, it will not be modified."
    ),
    responses={
        204: {"description": "Maintenance successfully updated"},
        400: {"description": "Invalid input or maintenance ID"},
        404: {"description": "Maintenance not found"},
        500: {"description": "Internal server error"},
    }
)
def edit_maintenance(
        maintenance_id: int = Path(..., description="Unique ID of the maintenance to edit", gt=0),
        request: MaintenanceDataRequest = ...
):
    """Passes the 'edit maintenance' request to the service"""
    logger.info(f"EDIT MAINTENANCE ROUTE HIT: {maintenance_id}")

    request_data = request.model_dump()
    request_data["maintenance_id"] = maintenance_id

    try:
        edit_maintenance_service(request_data)
        return Response(status_code=status.HTTP_204_NO_CONTENT)

    except IndexError as e:
        return Response(status_code=status.HTTP_404_NOT_FOUND, content=str(e))

    except ValueError as e:
        return Response(status_code=status.HTTP_400_BAD_REQUEST, content=str(e))

    except Exception as e:
        logger.error(f"Error while editing maintenance: {e}")
        raise HTTPException(status_code=500, detail="Internal server error")

@router.delete(
    "/{maintenance_id}",
    status_code=status.HTTP_204_NO_CONTENT,
    summary="Delete an maintenance",
        responses={
            204: {"description": "Maintenance successfully deleted"},
            400: {"description": "Invalid ID or bad request"},
            404: {"description": "Maintenance not found"},
            500: {"description": "Internal server error"}
        }
)
def remove_maintenance(
        maintenance_id: int = Path(..., description="Maintenance ID", gt=0),
):
    """Passes the 'remove maintenance' request to the service"""
    logger.info("REMOVE MAINTENANCE ROUTE HIT")
    try:
        remove_maintenance_service(maintenance_id)
        return Response(status_code=status.HTTP_204_NO_CONTENT)

    except IndexError as e:
        return Response(status_code=status.HTTP_404_NOT_FOUND, content=str(e))

    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))

    except Exception as e:
        logger.error(f"Error while removing maintenance: {e}")
        raise HTTPException(status_code=500, detail="Internal server error")