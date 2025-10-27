from pydantic import BaseModel

class AttachmentDataRequest(BaseModel):
    company_id: int | None = None
    user_id: int | None = None
    file_data: bytes | None = None
    file_type: str | None = None
    attachment_type: str | None = None
    upload_date: str | None = None