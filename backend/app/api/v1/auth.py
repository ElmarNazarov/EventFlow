from typing import Annotated

from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.api.deps import get_current_active_user, get_db
from app.models.user import User
from app.schemas.auth import LoginRequest, MessageResponse, TokenResponse
from app.schemas.user import UserRead
from app.services.auth_service import AuthService

router = APIRouter(prefix="/auth", tags=["auth"])


@router.post("/login", response_model=TokenResponse)
async def login(
    data: LoginRequest,
    db: Annotated[AsyncSession, Depends(get_db)],
) -> TokenResponse:
    service = AuthService(db)
    return await service.login(data)


@router.post("/logout", response_model=MessageResponse)
async def logout(
    _current_user: Annotated[User, Depends(get_current_active_user)],
) -> MessageResponse:
    return MessageResponse(message="Logged out successfully")


@router.get("/me", response_model=UserRead)
async def get_me(
    current_user: Annotated[User, Depends(get_current_active_user)],
) -> UserRead:
    return UserRead.model_validate(current_user)
