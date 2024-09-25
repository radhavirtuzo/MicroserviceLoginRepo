from pydantic import BaseModel

class LoginRequest(BaseModel):
    user_name: str
    user_password: str
