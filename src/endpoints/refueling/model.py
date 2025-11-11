from pydantic import BaseModel

class RefuelingDataRequest(BaseModel):
    refueling_id: int | None = None
    company_id: int | None = None
    user_id: int | None = None
    vehicle_id: int | None = None
    attachment_id: int | None = None
    refueling_type: str | None = None
    refueling_origin: str | None = None
    refueling_station: str | None = None
    current_kilometrage: int | None = None
    refueling_volume: float | None = None
    cost: float | None = None
    refueling_date: str | None = None
