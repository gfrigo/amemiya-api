from pydantic import BaseModel

class LoginDataRequest(BaseModel):
    email: str | None = None
    password: str | None = None