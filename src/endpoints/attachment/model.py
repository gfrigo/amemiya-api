from pydantic import BaseModel

class AttachmentDataRequest(BaseModel):
    company_id: int | None = None
    user_id: int | None = None
    user_name: str | None = None
    inner_register: str | None = None
    password: str | None = None
    email: str | None = None
    telephone: str | None = None
    role_id: int | None = None
    admin: bool | None = None
    company_id: int | None = None
    image_path: str | None = None
    active_user: bool | None = None