from datetime import datetime
from fastapi import APIRouter, UploadFile, File, Form, HTTPException, status, Path, Query
from fastapi.responses import Response, JSONResponse

from src.core.config import logger
from src.endpoints.attachment.model import AttachmentDataRequest
from src.endpoints.attachment.service import add_attachment_service
from .model import InvoiceDataRequest
from .service import fetch_invoice_service, add_invoice_service, edit_invoice_service, remove_invoice_service

router = APIRouter(prefix="/invoice", tags=["Invoice"])


@router.get(
    "/{company_id}",
    status_code=status.HTTP_200_OK,
    summary="Fetch invoices for a company",
    description=(
        "Retrieves all invoices associated with a specific company and found within the filter. "
        "Each invoice contains location details such as cost, origin and emission date."
    ),
    responses={
        200: {
            "description": "List of invoices successfully retrieved",
            "content": {
                "application/json": {
                    "data": [
                        {
                          "invoice_id": 3,
                          "company_id": 1,
                          "company_name": "root",
                          "user_id": 1,
                          "user_name": "Felipe Almeida de Carvalho",
                          "attachment_id": 24,
                          "file_data": "...",
                          "file_type": "pdf",
                          "upload_date": "2025-11-10 16:52:52",
                          "cost": 199.99,
                          "purchase_type": "online",
                          "invoice_origin": "store_a",
                          "invoice_number": "000000001",
                          "invoice_series": "A1",
                          "emission_date": "2025-11-10"
                        },
                        {
                          "invoice_id": 4,
                          "company_id": 1,
                          "company_name": "root",
                          "user_id": 1,
                          "user_name": "Felipe Almeida de Carvalho",
                          "attachment_id": 26,
                          "file_data": "...",
                          "file_type": "pdf",
                          "upload_date": "2025-11-10 17:29:08",
                          "cost": 299.99,
                          "purchase_type": "walmart",
                          "invoice_origin": "store_z",
                          "invoice_number": "001234567",
                          "invoice_series": "B7",
                          "emission_date": "2025-09-25"
                        }
                      ]
                }
            },
        },
        400: {"description": "Invalid company ID or bad request"},
        404: {"description": "No invoices found for the given company"},
        500: {"description": "Internal server error"},
    },
)
def fetch_invoice(
    company_id: int = Path(..., description="Unique ID of the company whose invoice should be retrieved", gt=0),
    user_id: int | None = Query(None, description="Unique ID of the user whose invoice are associated to", gt=0),
    cost_range_lower: float | None = Query(None, description="Minimum cost to filter invoices by", gt=0),
    cost_range_higher: float | None = Query(None, description="Maximum cost to filter invoices by", gt=0),
    purchase_type: str | None = Query(None, description="Specific purchase type to search"),
    invoice_origin: str | None = Query(None, description="Issuer or origin of the invoice"),
    contained_invoice_number: str | None = Query(None, description="Substring contained within the invoice number"),
    contained_invoice_series: str | None = Query(None, description="Substring contained within the invoice series"),
    emission_date_range_start: str | None = Query(None, description="Start of the date range to filter emission date by"),
    emission_date_range_end: str | None = Query(None, description="End of the date range to filter emission date by"),
):
    logger.info("FETCH INVOICE ROUTE HIT")

    request_data = {
        "company_id": company_id,
        "user_id": user_id,
        "cost_range_lower": cost_range_lower,
        "cost_range_higher": cost_range_higher,
        "purchase_type": purchase_type,
        "invoice_origin": invoice_origin,
        "contained_invoice_number": contained_invoice_number,
        "contained_invoice_series": contained_invoice_series,
        "emission_date_range_start": emission_date_range_start,
        "emission_date_range_end": emission_date_range_end
    }

    try:
        invoices_data: list = fetch_invoice_service(request_data)

        return JSONResponse(status_code=status.HTTP_200_OK, content={"data": invoices_data})

    except ValueError as e:
        return Response(status_code=status.HTTP_400_BAD_REQUEST, content=str(e))

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.post(
    "/{company_id}",
    status_code=status.HTTP_201_CREATED,
    summary="Add a new invoice",
    description=(
        "Creates a new invoice record associated with a given company. "
        "The invoice includes details such as cost, origin and emission date. "
        "Returns the ID of the newly created invoice upon success."
    ),
    responses={
        201: {
            "description": "Invoice successfully created",
            "content": {
                "application/json": {
                    "invoice_id": 1
                }
            },
        },
        400: {"description": "Invalid input data"},
        404: {"description": "Company not found"},
        500: {"description": "Internal server error"},
    },
)
async def add_invoice(
        company_id: int = Path(...),
        user_id: int = Form(...),
        file: UploadFile = File(...),
        file_type: str = Form(...),
        cost: float = Form(...),
        purchase_type: str = Form(...),
        invoice_origin: str = Form(...),
        invoice_number: str = Form(...),
        invoice_series: str = Form(...),
        emission_date: str = Form(...)
):
    """Passes the 'add invoice' request to the service"""
    logger.info("ADD INVOICE ROUTE HIT")

    file_bytes: bytes = await file.read()

    attachment_data_request = AttachmentDataRequest(
        uploaded_by_company_id=company_id,
        uploaded_by_user_id=user_id,
        file_data=file_bytes,
        file_type=file_type,
        attachment_type="invoice",
        upload_date=str(datetime.now())
    ).model_dump()

    try:
        attachment_id: int = add_attachment_service(attachment_data_request)
        if not attachment_id:
            return Response(status_code=status.HTTP_400_BAD_REQUEST)

        invoice_request_data = InvoiceDataRequest(
            company_id=company_id,
            user_id=user_id,
            attachment_id=attachment_id,
            cost=cost,
            purchase_type=purchase_type,
            invoice_origin=invoice_origin,
            invoice_number=invoice_number,
            invoice_series=invoice_series,
            emission_date=emission_date
        ).model_dump()

        invoice_id: int = add_invoice_service(invoice_request_data)

        return JSONResponse(status_code=status.HTTP_201_CREATED, content={"invoice_id": invoice_id})

    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))

    except Exception as e:
        logger.error(f"Error while adding invoice: {e}")
        raise HTTPException(status_code=500, detail="Internal server error")

@router.put(
"/{invoice_id}",
    status_code=status.HTTP_204_NO_CONTENT,
    summary="Edit an invoice",
    description=(
        "Updates an existing invoice record in the database. "
        "All fields provided in the request body will replace the existing values. "
        "If a field is omitted or set to `null`, it will not be modified."
    ),
    responses={
        204: {"description": "Invoice successfully updated"},
        400: {"description": "Invalid input or invoice ID"},
        404: {"description": "Invoice not found"},
        500: {"description": "Internal server error"},
    }
)
def edit_invoice(
        invoice_id: int = Path(..., description="Unique ID of the invoice to edit", gt=0),
        request: InvoiceDataRequest = ...
):
    """Passes the 'edit invoice' request to the service"""
    logger.info(f"EDIT INVOICE ROUTE HIT: {invoice_id}")

    request_data = request.model_dump()
    request_data["invoice_id"] = invoice_id

    try:
        edit_invoice_service(request_data)
        return Response(status_code=status.HTTP_204_NO_CONTENT)

    except IndexError as e:
        return Response(status_code=status.HTTP_404_NOT_FOUND, content=str(e))

    except ValueError as e:
        return Response(status_code=status.HTTP_400_BAD_REQUEST, content=str(e))

    except Exception as e:
        logger.error(f"Error while editing invoice: {e}")
        raise HTTPException(status_code=500, detail="Internal server error")

@router.delete(
    "/{invoice_id}",
    status_code=status.HTTP_204_NO_CONTENT,
    summary="Delete an invoice",
        responses={
            204: {"description": "Invoice successfully deleted"},
            400: {"description": "Invalid ID or bad request"},
            404: {"description": "Invoice not found"},
            500: {"description": "Internal server error"}
        }
)
def remove_invoice(
        invoice_id: int = Path(..., description="Invoice ID", gt=0),
):
    """Passes the 'remove invoice' request to the service"""
    logger.info("REMOVE INVOICE ROUTE HIT")
    try:
        remove_invoice_service(invoice_id)
        return Response(status_code=status.HTTP_204_NO_CONTENT)

    except IndexError as e:
        return Response(status_code=status.HTTP_404_NOT_FOUND, content=str(e))

    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))

    except Exception as e:
        logger.error(f"Error while removing invoice: {e}")
        raise HTTPException(status_code=500, detail="Internal server error")