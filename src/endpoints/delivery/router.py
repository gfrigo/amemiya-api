from fastapi import APIRouter, UploadFile, Path, Query, Body, File, Form, HTTPException, status
from fastapi.responses import Response, JSONResponse
from src.core.logging_config import logger
from .model import DeliveryDataRequest
from .service import fetch_delivery_service, add_delivery_service, edit_delivery_service, remove_delivery_service
from datetime import datetime

router = APIRouter(prefix="/delivery", tags=["Delivery"])

@router.get("/{company_id}", status_code=status.HTTP_200_OK)
def fetch_delivery(
        company_id: int = Path(..., description="Unique ID of the company whose deliveries should be retrieved", gt=0),
        user_id: int | None = Query(None, description="Unique ID of the user whose deliveries are associated to", gt=0),
        vehicle_id: int | None = Query(None, description="Unique ID of the vehicle whose deliveries are associated to", gt=0),
        delivery_code: str | None = Query(None, description="Substring unique Delivery Code to search by"),
        payload_item: str | None = Query(None, description="Substring payload item to search by"),
        payload_quantity_range_lower: float | None = Query(None, description="Minimum item quantity to filter by", gt=0),
        payload_quantity_range_higher: float | None = Query(None, description="Maximum item quantity to filter by", gt=0),
        payload_quantity_unit: str | None = Query(None, description="Payload item quantity unit to search by"),
        payload_weight_range_lower: float | None = Query(None, description="Minimum item weight to filter by", gt=0),
        payload_weight_range_higher: float | None = Query(None, description="Maximum item weight to filter by", gt=0),
        estimated_delivery_time_date_range_start: str | None = Query(None, description="Start of the estimated delivery time range to filter deliveries by"),
        estimated_delivery_time_date_range_end: str | None = Query(None, description="End of the estimated delivery time range to filter deliveries by"),
        start_time_date_range_start: str | None = Query(None, description="Start of the delivery start time range to filter deliveries by"),
        start_time_date_range_end: str | None = Query(None, description="End of the delivery start time range to filter deliveries by"),
        start_label: str | None = Query(None, description="Label of the delivery start location to filter deliveries by"),
        start_city: str | None = Query(None, description="City of the delivery start location to filter deliveries by"),
        start_district: str | None = Query(None, description="District of the delivery start location to filter deliveries by"),
        finish_time_date_range_start: str | None = Query(None, description="Start of the delivery end time range to filter deliveries by"),
        finish_time_date_range_end: str | None = Query(None, description="End of the delivery end time range to filter deliveries by"),
        end_label: str | None = Query(None, description="Label of the delivery end location to filter deliveries by"),
        end_city: str | None = Query(None, description="City of the delivery end location to filter deliveries by"),
        end_district: str | None = Query(None, description="District of the delivery end location to filter deliveries by"),
        delivery_status: str | None = Query(None, description="Delivery status to filter deliveries by"),
    ):
    logger.info("FETCH DELIVERY ROUTE HIT")

    request_data = {
        "company_id": company_id,
        "user_id": user_id,
        "vehicle_id": vehicle_id,
        "delivery_code": delivery_code,
        "payload_item": payload_item,
        "payload_quantity_range_lower": payload_quantity_range_lower,
        "payload_quantity_range_higher": payload_quantity_range_higher,
        "payload_quantity_unit": payload_quantity_unit,
        "payload_weight_range_lower": payload_weight_range_lower,
        "payload_weight_range_higher": payload_weight_range_higher,
        "estimated_delivery_time_date_range_start": estimated_delivery_time_date_range_start,
        "estimated_delivery_time_date_range_end": estimated_delivery_time_date_range_end,
        "start_time_date_range_start": start_time_date_range_start,
        "start_time_date_range_end": start_time_date_range_end,
        "start_label": start_label,
        "start_city": start_city,
        "start_district": start_district,
        "finish_time_date_range_start": finish_time_date_range_start,
        "finish_time_date_range_end": finish_time_date_range_end,
        "end_label": end_label,
        "end_city": end_city,
        "end_district": end_district,
        "delivery_status": delivery_status
    }

    try:
        deliveries_data: list = fetch_delivery_service(request_data)

        return JSONResponse(status_code=status.HTTP_200_OK, content={"data": deliveries_data})

    except ValueError as e:
        return Response(status_code=status.HTTP_400_BAD_REQUEST, content=str(e))

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.post(
    "/{company_id}",
    status_code=status.HTTP_201_CREATED,
    summary="Add a new delivery",
    description=(
        "Creates a new delivery record associated with a given company. "
        "The delivery includes details such as associated starting and end point, status and estimated delivery time. "
        "Returns the ID of the newly created delivery upon success."
    ),
    responses={
        201: {
            "description": "Delivery successfully created",
            "content": {
                "application/json": {
                    "delivery_id": 1
                }
            },
        },
        400: {"description": "Invalid input data"},
        404: {"description": "Company not found"},
        500: {"description": "Internal server error"},
    },
)
def add_delivery(
        company_id: int = Path(...),
        request: DeliveryDataRequest = ...,
):
    """Passes the 'add delivery' request to the service"""
    logger.info("ADD DELIVERY ROUTE HIT")

    delivery_data_request = request.model_dump()
    delivery_data_request["company_id"] = company_id

    try:
        delivery_id: int = add_delivery_service(delivery_data_request)
        if not delivery_id:
            return Response(status_code=status.HTTP_400_BAD_REQUEST)

        return JSONResponse(status_code=status.HTTP_201_CREATED, content={"delivery_id": delivery_id})

    except ValueError as e:
        return Response(status_code=status.HTTP_400_BAD_REQUEST, content=str(e))

    except IndexError as e:
        return Response(status_code=status.HTTP_404_NOT_FOUND, content=str(e))

    except RuntimeError as e:
        return Response(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, content=str(e))

    except Exception as e:
        logger.error(f"Error while adding delivery: {e}")
        raise HTTPException(status_code=500, detail="Internal server error")

@router.put(
"/{delivery_id}",
    status_code=status.HTTP_204_NO_CONTENT,
    summary="Edit a delivery",
    description=(
        "Updates an existing delivery record in the database. "
        "All fields provided in the request body will replace the existing values. "
        "If a field is omitted or set to `null`, it will not be modified."
    ),
    responses={
        204: {"description": "Delivery successfully updated"},
        400: {"description": "Invalid input or delivery ID"},
        404: {"description": "Delivery not found"},
        500: {"description": "Internal server error"},
    }
)
def edit_delivery(
        delivery_id: int = Path(..., description="Unique ID of the delivery to edit", gt=0),
        request: DeliveryDataRequest = ...
):
    """Passes the 'edit delivery' request to the service"""
    logger.info(f"EDIT DELIVERY ROUTE HIT: {delivery_id}")

    request_data = request.model_dump()
    request_data["delivery_id"] = delivery_id

    try:
        edit_delivery_service(request_data)
        return Response(status_code=status.HTTP_204_NO_CONTENT)

    except IndexError as e:
        return Response(status_code=status.HTTP_404_NOT_FOUND, content=str(e))

    except ValueError as e:
        return Response(status_code=status.HTTP_400_BAD_REQUEST, content=str(e))

    except Exception as e:
        logger.error(f"Error while editing delivery: {e}")
        raise HTTPException(status_code=500, detail="Internal server error")


@router.delete(
    "/{delivery_id}",
    status_code=status.HTTP_204_NO_CONTENT,
    summary="Delete a delivery",
        responses={
            204: {"description": "Delivery successfully deleted"},
            400: {"description": "Invalid ID or bad request"},
            404: {"description": "Delivery not found"},
            500: {"description": "Internal server error"}
        }
)
def remove_delivery(
        delivery_id: int = Path(..., description="Delivery ID", gt=0),
):
    """Passes the 'remove delivery' request to the service"""
    logger.info("REMOVE DELIVERY ROUTE HIT")
    try:
        remove_delivery_service(delivery_id)
        return Response(status_code=status.HTTP_204_NO_CONTENT)

    except IndexError as e:
        return Response(status_code=status.HTTP_404_NOT_FOUND, content=str(e))

    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))

    except Exception as e:
        logger.error(f"Error while removing delivery: {e}")
        raise HTTPException(status_code=500, detail="Internal server error")