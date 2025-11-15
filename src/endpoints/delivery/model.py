from pydantic import BaseModel

class DeliveryDataRequest(BaseModel):
    delivery_id: int | None = None
    company_id: int | None = None
    user_id: int | None = None
    vehicle_id: int | None = None
    delivery_code: str | None = None
    payload_item: str | None = None
    payload_quantity: float | None = None
    payload_quantity_unit: str | None = None
    payload_weight: float | None = None
    estimated_delivery_time: str | None = None
    start_geopoint_id: int | None = None
    start_latitude: float | None = None
    start_longitude: float | None = None
    end_geopoint_id: int | None = None
    end_latitude: float | None = None
    end_longitude: float | None = None
    delivery_status: str | None = None
