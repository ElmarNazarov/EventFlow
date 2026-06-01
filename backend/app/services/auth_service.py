from sqlalchemy.ext.asyncio import AsyncSession

from app.core.exceptions import AppException
from app.core.security import create_access_token, hash_password, verify_password
from app.repositories.users import UserRepository
from app.schemas.auth import LoginRequest, TokenResponse
from app.schemas.user import UserCreate, UserRead


class AuthService:
    def __init__(self, db: AsyncSession) -> None:
        self.db = db
        self.users = UserRepository(db)

    async def login(self, data: LoginRequest) -> TokenResponse:
        user = await self.users.get_by_email(data.email)
        if user is None or not verify_password(data.password, user.hashed_password):
            raise AppException("Invalid email or password", status_code=401)
        if not user.is_active:
            raise AppException("User account is inactive", status_code=403)

        token = create_access_token(
            subject=str(user.id),
            extra_claims={"role": user.role.value, "email": user.email},
        )
        return TokenResponse(access_token=token)

    async def get_current_user_profile(self, user_id: int) -> UserRead:
        user = await self.users.get_by_id(user_id)
        if user is None:
            raise AppException("User not found", status_code=404)
        return UserRead.model_validate(user)

    async def register_user(self, data: UserCreate) -> UserRead:
        if await self.users.email_exists(data.email):
            raise AppException("Email already registered", status_code=400)

        user = await self.users.create(
            email=data.email,
            hashed_password=hash_password(data.password),
            full_name=data.full_name,
            role=data.role,
            is_active=data.is_active,
        )
        await self.db.commit()
        return UserRead.model_validate(user)
