from pydantic import BaseModel

class LoginDataRequest(BaseModel):
    user_name: str | None = None
    password: str | None = None