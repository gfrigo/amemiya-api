from pydantic import BaseModel

class RouteDataRequest(BaseModel):
    company_id: int | None = None
    user_id: int | None = None
    creation_datetime: str | None = None
    subroutes: list | None = None
