from typing import Annotated

from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.api.deps import get_current_active_user, get_db, require_user_management
from app.models.user import User
from app.schemas.user import UserCreate, UserRead
from app.services.auth_service import AuthService

router = APIRouter(prefix="/users", tags=["users"])


@router.get("/me", response_model=UserRead)
async def get_current_user_profile(
    current_user: Annotated[User, Depends(get_current_active_user)],
) -> UserRead:
    return UserRead.model_validate(current_user)


@router.get("", response_model=list[UserRead])
async def list_users(
    _admin: Annotated[User, Depends(require_user_management)],
    db: Annotated[AsyncSession, Depends(get_db)],
) -> list[UserRead]:
    from app.repositories.users import UserRepository

    users = await UserRepository(db).list_users()
    return [UserRead.model_validate(u) for u in users]


@router.post("", response_model=UserRead, status_code=201)
async def create_user(
    data: UserCreate,
    _admin: Annotated[User, Depends(require_user_management)],
    db: Annotated[AsyncSession, Depends(get_db)],
) -> UserRead:
    service = AuthService(db)
    return await service.register_user(data)
