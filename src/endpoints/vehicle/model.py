from pydantic import BaseModel

class VehicleDataRequest(BaseModel):
    vehicle_id: int | None = None
    company_id: int | None = None
    name: str | None = None
    license_plate: str | None = None
    brand: str | None = None
    model: str | None = None
    year: int | None = None
    notes: str | None = None
    last_used: str | None = None
    last_user_id: int | None = None
    active: bool | None = None