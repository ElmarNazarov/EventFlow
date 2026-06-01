from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.constants import UserRole
from app.models.user import User


class UserRepository:
    def __init__(self, db: AsyncSession) -> None:
        self.db = db

    async def get_by_id(self, user_id: int) -> User | None:
        result = await self.db.execute(select(User).where(User.id == user_id))
        return result.scalar_one_or_none()

    async def get_by_email(self, email: str) -> User | None:
        result = await self.db.execute(select(User).where(User.email == email.lower()))
        return result.scalar_one_or_none()

    async def list_users(self) -> list[User]:
        result = await self.db.execute(select(User).order_by(User.id))
        return list(result.scalars().all())

    async def create(
        self,
        *,
        email: str,
        hashed_password: str,
        full_name: str,
        role: UserRole,
        is_active: bool = True,
    ) -> User:
        user = User(
            email=email.lower(),
            hashed_password=hashed_password,
            full_name=full_name,
            role=role,
            is_active=is_active,
        )
        self.db.add(user)
        await self.db.flush()
        await self.db.refresh(user)
        return user

    async def email_exists(self, email: str) -> bool:
        user = await self.get_by_email(email)
        return user is not None
