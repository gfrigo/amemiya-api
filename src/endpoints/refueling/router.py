from fastapi import APIRouter, UploadFile, File, Form, HTTPException, status, Path, Query
from fastapi.responses import Response, JSONResponse
from src.core.logging_config import logger
from .model import RefuelingDataRequest
from src.endpoints.attachment.model import AttachmentDataRequest
from .service import fetch_refueling_service, add_refueling_service, edit_refueling_service, remove_refueling_service
from src.endpoints.attachment.service import add_attachment_service
from datetime import datetime

router = APIRouter(prefix="/refueling", tags=["Refueling"])


@router.get(
    "/{company_id}",
    status_code=status.HTTP_200_OK,
    summary="Fetch refuelings for a company",
    description=(
        "Retrieves all refuelings associated with a specific company and found within the filter. "
        "Each refuelings contains location details such as associated vehicle, date and volume."
    ),
    responses={
        200: {
            "description": "List of refuelings successfully retrieved",
            "content": {
                "application/json": {
                    "data": [

                      ]
                }
            },
        },
        400: {"description": "Invalid company ID or bad request"},
        404: {"description": "No refuelings found for the given company"},
        500: {"description": "Internal server error"},
    },
)
def fetch_refueling(
    company_id: int = Path(..., description="Unique ID of the company whose refuelings should be retrieved", gt=0),
    user_id: int | None = Query(None, description="Unique ID of the user whose refuelings are associated to", gt=0),
    vehicle_id: int | None = Query(None, description="Unique ID of the vehicle whose refuelings are associated to", gt=0),
    refueling_type: str | None = Query(None, description="Specific refuelings type to search for"),
    refueling_origin: str | None = Query(None, description="Place of origin of the refuelings"),
    refueling_station: str | None = Query(None, description="Gas Station of the refuelings"),
    kilometrage_range_lower: int | None = Query(None, description="Minimum kilometrage to filter refuelings by"),
    kilometrage_range_higher: int | None = Query(None, description="Maximum kilometrage to filter refuelings by"),
    volume_range_lower: float | None = Query(None, description="Minimum volume to filter refuelings by"),
    volume_range_higher: float | None = Query(None, description="Maximum volume to filter refuelings by"),
    cost_range_lower: float | None = Query(None, description="Minimum cost to filter refuelings by", gt=0),
    cost_range_higher: float | None = Query(None, description="Maximum cost to filter refuelings by", gt=0),
    refueling_date_range_start: str | None = Query(None, description="Start of the date range to filter refuelings date by"),
    refueling_date_range_end: str | None = Query(None, description="End of the date range to filter refuelings date by"),
):
    logger.info("FETCH REFUELING ROUTE HIT")

    request_data = {
        "company_id": company_id,
        "user_id": user_id,
        "vehicle_id": vehicle_id,
        "refueling_type": refueling_type,
        "refueling_origin": refueling_origin,
        "refueling_station": refueling_station,
        "kilometrage_range_lower": kilometrage_range_lower,
        "kilometrage_range_higher": kilometrage_range_higher,
        "volume_range_lower": volume_range_lower,
        "volume_range_higher": volume_range_higher,
        "cost_range_lower": cost_range_lower,
        "cost_range_higher": cost_range_higher,
        "refueling_date_range_start": refueling_date_range_start,
        "refueling_date_range_end": refueling_date_range_end
    }

    try:
        refuelings_data: list = fetch_refueling_service(request_data)

        return JSONResponse(status_code=status.HTTP_200_OK, content={"data": refuelings_data})

    except ValueError as e:
        return Response(status_code=status.HTTP_400_BAD_REQUEST, content=str(e))

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.post(
    "/{company_id}",
    status_code=status.HTTP_201_CREATED,
    summary="Add a new refueling",
    description=(
        "Creates a new refueling record associated with a given company. "
        "The refueling includes details such as associated vehicle, date and volume. "
        "Returns the ID of the newly created refueling upon success."
    ),
    responses={
        201: {
            "description": "Refueling successfully created",
            "content": {
                "application/json": {
                    "refueling_id": 1
                }
            },
        },
        400: {"description": "Invalid input data"},
        404: {"description": "Company not found"},
        500: {"description": "Internal server error"},
    },
)
async def add_refueling(
        company_id: int = Path(...),
        user_id: int = Form(...),
        vehicle_id: int = Form(...),
        file: UploadFile = File(...),
        file_type: str = Form(...),
        refueling_type: str = Form(...),
        refueling_origin: str = Form(...),
        refueling_station: str = Form(...),
        current_kilometrage: int = Form(...),
        refueling_volume: float = Form(...),
        cost: float = Form(...),
        refueling_date: str = Form(...)
):
    """Passes the 'add refueling' request to the service"""
    logger.info("ADD REFUELING ROUTE HIT")

    file_bytes: bytes = await file.read()

    attachment_data_request = AttachmentDataRequest(
        uploaded_by_company_id=company_id,
        uploaded_by_user_id=user_id,
        file_data=file_bytes,
        file_type=file_type,
        attachment_type="refueling",
        upload_date=str(datetime.now())
    ).model_dump()

    try:
        attachment_id: int = add_attachment_service(attachment_data_request)
        if not attachment_id:
            return Response(status_code=status.HTTP_400_BAD_REQUEST)

        refueling_data_request = RefuelingDataRequest(
            company_id=company_id,
            user_id=user_id,
            vehicle_id=vehicle_id,
            attachment_id=attachment_id,
            refueling_type=refueling_type,
            refueling_origin=refueling_origin,
            refueling_station=refueling_station,
            current_kilometrage=current_kilometrage,
            refueling_volume=refueling_volume,
            cost=cost,
            refueling_date=refueling_date
        ).model_dump()

        refueling_id: int = add_refueling_service(refueling_data_request)

        return JSONResponse(status_code=status.HTTP_201_CREATED, content={"refueling_id": refueling_id})

    except ValueError as e:
        return Response(status_code=status.HTTP_400_BAD_REQUEST, content=str(e))

    except Exception as e:
        logger.error(f"Error while adding refueling: {e}")
        raise HTTPException(status_code=500, detail="Internal server error")

@router.put(
"/{refueling_id}",
    status_code=status.HTTP_204_NO_CONTENT,
    summary="Edit a refueling",
    description=(
        "Updates an existing refueling record in the database. "
        "All fields provided in the request body will replace the existing values. "
        "If a field is omitted or set to `null`, it will not be modified."
    ),
    responses={
        204: {"description": "Refueling successfully updated"},
        400: {"description": "Invalid input or refueling ID"},
        404: {"description": "Refueling not found"},
        500: {"description": "Internal server error"},
    }
)
def edit_refueling(
        refueling_id: int = Path(..., description="Unique ID of the refueling to edit", gt=0),
        request: RefuelingDataRequest = ...
):
    """Passes the 'edit refueling' request to the service"""
    logger.info(f"EDIT REFUELING ROUTE HIT: {refueling_id}")

    request_data = request.model_dump()
    request_data["refueling_id"] = refueling_id

    try:
        edit_refueling_service(request_data)
        return Response(status_code=status.HTTP_204_NO_CONTENT)

    except IndexError as e:
        return Response(status_code=status.HTTP_404_NOT_FOUND, content=str(e))

    except ValueError as e:
        return Response(status_code=status.HTTP_400_BAD_REQUEST, content=str(e))

    except Exception as e:
        logger.error(f"Error while editing refueling: {e}")
        raise HTTPException(status_code=500, detail="Internal server error")

@router.delete(
    "/{refueling_id}",
    status_code=status.HTTP_204_NO_CONTENT,
    summary="Delete a refueling",
        responses={
            204: {"description": "Refueling successfully deleted"},
            400: {"description": "Invalid ID or bad request"},
            404: {"description": "Refueling not found"},
            500: {"description": "Internal server error"}
        }
)
def remove_refueling(
        refueling_id: int = Path(..., description="Refueling ID", gt=0),
):
    """Passes the 'remove refueling' request to the service"""
    logger.info("REMOVE REFUELING ROUTE HIT")
    try:
        remove_refueling_service(refueling_id)
        return Response(status_code=status.HTTP_204_NO_CONTENT)

    except IndexError as e:
        return Response(status_code=status.HTTP_404_NOT_FOUND, content=str(e))

    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))

    except Exception as e:
        logger.error(f"Error while removing refueling: {e}")
        raise HTTPException(status_code=500, detail="Internal server error")