from pydantic import BaseModel, Field

from app.schemas.common import EmailStrLocal


class LoginRequest(BaseModel):
    email: EmailStrLocal
    password: str = Field(min_length=6)


class TokenResponse(BaseModel):
    access_token: str
    token_type: str = "bearer"


class MessageResponse(BaseModel):
    message: str
