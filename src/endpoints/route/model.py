from pydantic import BaseModel

class RouteDataRequest(BaseModel):
    created_by_company_id: int | None = None
    created_by_user_id: int | None = None
    creation_datetime: str | None = None
    subroutes: list | dict | None = None
    country: str | None = None
    state: str | None = None
    city: str | None = None
    district: str | None = None
