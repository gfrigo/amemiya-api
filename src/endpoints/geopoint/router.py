from fastapi import APIRouter, HTTPException, status, Path, Query
from fastapi.responses import Response, JSONResponse

from src.core.config import logger
from .model import GeopointDataRequest
from .service import fetch_geopoint_service, add_geopoint_service, edit_geopoint_service, remove_geopoint_service

router = APIRouter(prefix="/geopoint", tags=["Geopoint"])


@router.get(
    "/{company_id}",
    status_code=status.HTTP_200_OK,
    summary="Fetch geopoints for a company",
    description=(
        "Retrieves all geopoints associated with a specific company. "
        "Each geopoint contains location details such as latitude, longitude, label, and type."
    ),
    responses={
        200: {
            "description": "List of geopoints successfully retrieved",
            "content": {
                "application/json": {
                    "origin": [
                        {
                            "geopoint_id": 1,
                            "label": "Warehouse A",
                            "latitude": -23.5505,
                            "longitude": -46.6333,
                            "city": "São Paulo",
                            "state": "SP",
                            "country": "Brazil",
                            "type": "origin"
                        }
                    ],
                    "destiny": [
                        {
                            "geopoint_id": 2,
                            "label": "Warehouse B",
                            "latitude": -23.5504,
                            "longitude": -46.6332,
                            "city": "São Paulo",
                            "state": "SP",
                            "country": "Brazil",
                            "type": "origin"
                        }
                    ]
                }
            },
        },
        400: {"description": "Invalid company ID or bad request"},
        404: {"description": "No geopoints found for the given company"},
        500: {"description": "Internal server error"},
    },
)
def fetch_geopoint(
    company_id: int = Path(..., description="Unique ID of the company whose geopoints should be retrieved", gt=0),
    geopoint_id: int | None = Query(None, description="Unique ID of the geopoint to retrieve", gt=0),
):
    logger.info("FETCH GEOPOINT ROUTE HIT")

    request_data = {
        "company_id": company_id,
        "geopoint_id": geopoint_id
    }

    try:
        geopoints = fetch_geopoint_service(request_data)

        return JSONResponse(status_code=status.HTTP_200_OK, content=geopoints)

    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.post(
    "/{company_id}",
    status_code=status.HTTP_201_CREATED,
    summary="Add a new geopoint",
    description=(
        "Creates a new geopoint record associated with a given company. "
        "The geopoint includes details such as coordinates, label, and type. "
        "Returns the ID of the newly created geopoint upon success."
    ),
    responses={
        201: {
            "description": "Geopoint successfully created",
            "content": {
                "application/json": {
                    "geopoint_id": 1
                }
            },
        },
        400: {"description": "Invalid input data"},
        404: {"description": "Company not found"},
        500: {"description": "Internal server error"},
    },
)
def add_geopoint(
    company_id: int = Path(..., description="Unique ID of the company to associate the geopoint with", gt=0),
    request: GeopointDataRequest = ...,
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

@router.put(
"/{geopoint_id}",
    status_code=status.HTTP_204_NO_CONTENT,
    summary="Edit a geopoint",
    description=(
        "Updates an existing geopoint record in the database. "
        "All fields provided in the request body will replace the existing values. "
        "If a field is omitted or set to `null`, it will not be modified."
    ),
    responses={
        204: {"description": "Geopoint successfully updated"},
        400: {"description": "Invalid input or geopoint ID"},
        404: {"description": "Geopoint not found"},
        500: {"description": "Internal server error"},
    }
)
def edit_geopoint(
        geopoint_id: int = Path(..., description="Unique ID of the geopoint to edit", gt=0),
        request: GeopointDataRequest = ...
):
    """Passes the 'edit geopoint' request to the service"""
    logger.info(f"EDIT GEOPOINT ROUTE HIT: {geopoint_id}")

    request_data = request.model_dump()
    request_data["geopoint_id"] = geopoint_id

    try:
        edit_geopoint_service(request_data)
        return Response(status_code=status.HTTP_204_NO_CONTENT)

    except IndexError as e:
        return Response(status_code=status.HTTP_404_NOT_FOUND, content=str(e))

    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))

    except Exception as e:
        logger.error(f"Error while editing geopoint: {e}")
        raise HTTPException(status_code=500, detail="Internal server error")

@router.delete(
    "/{geopoint_id}",
    status_code=status.HTTP_204_NO_CONTENT,
    summary="Delete a geopoint",
        responses={
            204: {"description": "Geopoint successfully deleted"},
            400: {"description": "Invalid ID or bad request"},
            404: {"description": "Geopoint not found"},
            500: {"description": "Internal server error"}
        }
)
def remove_geopoint(
        geopoint_id: int = Path(..., description="Geopoint ID", gt=0),
):
    """Passes the 'remove geopoint' request to the service"""
    logger.info("REMOVE GEOPOINT ROUTE HIT")
    try:
        remove_geopoint_service(geopoint_id)
        return Response(status_code=status.HTTP_204_NO_CONTENT)

    except IndexError as e:
        return Response(status_code=status.HTTP_404_NOT_FOUND, content=str(e))

    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))

    except Exception as e:
        logger.error(f"Error while removing geopoint: {e}")
        raise HTTPException(status_code=500, detail="Internal server error")