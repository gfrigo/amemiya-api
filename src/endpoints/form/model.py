from pydantic import BaseModel

class FormDataRequest(BaseModel):
    form_id: int | None = None
    company_id: int | None = None
    user_id: int | None = None
    delivery_id: int | None = None
    description: str | None = None
    was_delivered: bool | None = None
    had_problem: bool | None = None
    problem_description: str | None = None
    who_received: str | None = None
    creation_datetime: str | None = None
    notes: str | None = None
