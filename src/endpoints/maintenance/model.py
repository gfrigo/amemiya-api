from pydantic import BaseModel

class MaintenanceDataRequest(BaseModel):
    maintenance_id: int | None = None
    company_id: int | None = None
    user_id: int | None = None
    vehicle_id: int | None = None
    attachment_id: int | None = None
    maintenance_type: str | None = None
    maintenance_origin: str | None = None
    maintenance_responsible: str | None = None
    cost: float | None = None
    maintenance_date: str | None = None
