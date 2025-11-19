from datetime import datetime

from fastapi import APIRouter, Query, Path, HTTPException, status
from fastapi.responses import Response, JSONResponse

from src.core.config import logger
from .model import FormDataRequest
from .service import fetch_form_service, add_form_service, edit_form_service, remove_form_service

router = APIRouter(prefix="/form", tags=["Form"])

@router.get(
    "/{company_id}",
    status_code=status.HTTP_200_OK,
    summary="Fetch forms for a company",
    description=(
            "Retrieves all forms associated with a specific company and found within the filter. "
            "Each form contains location details such as associated delivery, description and date."
    ),
    responses={
        200: {
            "description": "List of Forms successfully retrieved",
            "content": {
                "application/json": {
                    "data":[
                        {
                            "form_id":1,
                            "company_id":1,
                            "company_name":"root",
                            "user_id":1,
                            "user_name":"Felipe Almeida de Carvalho",
                            "delivery_id":1,
                            "delivery_code":"ROOT-4fb4dcf3b8",
                            "description":"teste",
                            "was_delivered":True,
                            "had_problem":False,
                            "problem_description":None,
                            "who_received":"José Carlos",
                            "creation_datetime":"2025-11-13 14:15:19",
                            "notes":"nothing"
                        }
                    ]
                }
            },
        },
        400: {"description": "Invalid company ID or bad request"},
        404: {"description": "No forms found for the given company"},
        500: {"description": "Internal server error"},
    },
)
def fetch_form(
        company_id: int = Path(..., description="Unique ID of the company whose forms should be retrieved", gt=0),
        user_id: int | None = Query(None, description="Unique ID of the user whose forms are associated to", gt=0),
        delivery_code: str | None = Query(None, description="Specific delivery code to search for"),
        was_delivered: bool | None = Query(None, description="Whether the delivery was delivered or not"),
        had_problem: bool | None = Query(None, description="Whether the delivery had a problem or not"),
        who_received: str | None = Query(None, description="Receiver of the delivery"),
        creation_datetime_range_start: str | None = Query(None, description="Start of the creation date range to filter forms by"),
        creation_datetime_range_end: str | None = Query(None, description="End of the creation date range to filter forms by"),
    ):
    logger.info("FETCH FORM ROUTE HIT")

    request_data = {
        "company_id": company_id,
        "user_id": user_id,
        "delivery_code": delivery_code,
        "was_delivered": was_delivered,
        "had_problem": had_problem,
        "who_received": who_received,
        "creation_datetime_range_start": creation_datetime_range_start,
        "creation_datetime_range_end": creation_datetime_range_end
    }

    try:
        forms_data: list = fetch_form_service(request_data)

        if forms_data:
            return JSONResponse(status_code=status.HTTP_200_OK, content={"data": forms_data})

        return Response(status_code=status.HTTP_204_NO_CONTENT)

    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.post(
    "/{company_id}",
    status_code=status.HTTP_201_CREATED,
    summary="Add a new form",
    description=(
        "Creates a new form record associated with a given company. "
        "The form includes details such as associated delivery, who received it and description. "
        "Returns the ID of the newly created form upon success."
    ),
    responses={
        201: {
            "description": "Form successfully created",
            "content": {
                "application/json": {
                    "form_id": 1
                }
            },
        },
        400: {"description": "Invalid input data"},
        404: {"description": "Company not found"},
        500: {"description": "Internal server error"},
    },
)
def add_form(
        company_id: int = Path(..., description="Company ID to associate the form to", gt=0),
        request: FormDataRequest = ...
):
    """Passes the 'add form' request to the service"""
    logger.info("ADD FORM ROUTE HIT")

    request_data = request.model_dump()
    request_data["company_id"] = company_id
    request_data["creation_datetime"] = str(datetime.now())

    try:
        form_id: int = add_form_service(request_data)

        if not form_id:
            return Response(status_code=status.HTTP_400_BAD_REQUEST)

        return JSONResponse(status_code=status.HTTP_201_CREATED, content={"form_id": form_id})

    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Internal server error {str(e)}")


@router.put(
"/{form_id}",
    status_code=status.HTTP_204_NO_CONTENT,
    summary="Edit a form",
    description=(
        "Updates an existing form record in the database. "
        "All fields provided in the request body will replace the existing values. "
        "If a field is omitted or set to `null`, it will not be modified."
    ),
    responses={
        204: {"description": "Form successfully updated"},
        400: {"description": "Invalid input or form ID"},
        404: {"description": "Form not found"},
        500: {"description": "Internal server error"},
    }
)
def edit_form(
        form_id: int = Path(..., description="Unique ID of the form to edit", gt=0),
        request: FormDataRequest = ...
    ):
    logger.info("EDIT FORM ROUTE HIT")

    request_data = request.model_dump()
    request_data["form_id"] = form_id

    try:
        edit_form_service(request_data)
        return Response(status_code=status.HTTP_204_NO_CONTENT)

    except IndexError as e:
        return Response(status_code=status.HTTP_404_NOT_FOUND, content=str(e))

    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Internal server error {str(e)}")

@router.delete("/{form_id}")
def remove_form(
        form_id: int = Path(..., description="Form ID", gt=0)
):
    logger.info("REMOVE FORM ROUTE HIT")

    request_data = {"form_id": form_id}

    try:
        remove_form_service(request_data)

        return Response(status_code=status.HTTP_204_NO_CONTENT)

    except IndexError as e:
        return Response(status_code=status.HTTP_404_NOT_FOUND, content=str(e))

    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Internal server error {e}")