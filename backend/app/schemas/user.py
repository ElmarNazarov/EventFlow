from datetime import datetime

from pydantic import BaseModel, ConfigDict, Field

from app.core.constants import UserRole
from app.schemas.common import EmailStrLocal


class UserBase(BaseModel):
    email: EmailStrLocal
    full_name: str = Field(min_length=1, max_length=255)
    role: UserRole
    is_active: bool = True


class UserCreate(UserBase):
    password: str = Field(min_length=6)


class UserRead(UserBase):
    model_config = ConfigDict(from_attributes=True)

    id: int
    created_at: datetime
    updated_at: datetime


class UserUpdate(BaseModel):
    full_name: str | None = None
    role: UserRole | None = None
    is_active: bool | None = None
    password: str | None = Field(default=None, min_length=6)
