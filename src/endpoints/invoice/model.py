from pydantic import BaseModel

class GeopointDataRequest(BaseModel):
    company_id: int | None = None
    point_id: int | None = None
    user_id: int | None = None
    label: str | None = None
    longitude: float | None = None
    latitude: float | None = None
    geopoint_type: str | None = None
    country: str | None = None
    state: str | None = None
    city: str | None = None
    district: str | None = None
