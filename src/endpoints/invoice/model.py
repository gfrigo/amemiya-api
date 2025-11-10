from pydantic import BaseModel

class InvoiceDataRequest(BaseModel):
    invoice_id: int | None = None
    company_id: int | None = None
    user_id: int | None = None
    attachment_id: int | None = None
    cost: float | None = None
    purchase_type: str | None = None
    invoice_origin: str | None = None
    invoice_number: str | None = None
    invoice_series: str | None = None
    emission_date: str | None = None
