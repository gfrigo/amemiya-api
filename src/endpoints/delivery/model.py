from pydantic import BaseModel

class DeliveryDataRequest(BaseModel):
    delivery_id: int | None = None
    user_id: int | None = None
    vehicle_id: int | None = None
    route_id: int | None = None
    finish_time: str | None = None
    load_name: str | None = None
    start_time: str | None = None
    status: str | None = None


