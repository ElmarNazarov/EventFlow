"""Seed demo users for local development."""

import asyncio
import logging

from sqlalchemy import select

from app.core.constants import UserRole
from app.core.database import AsyncSessionLocal
from app.core.security import hash_password
from app.models.user import User

logger = logging.getLogger(__name__)

DEMO_USERS = [
    {
        "email": "admin@eventflow.local",
        "password": "password123",
        "full_name": "Admin User",
        "role": UserRole.ADMIN,
    },
    {
        "email": "ops@eventflow.local",
        "password": "password123",
        "full_name": "Ops Manager",
        "role": UserRole.OPS_MANAGER,
    },
    {
        "email": "support@eventflow.local",
        "password": "password123",
        "full_name": "Support Agent",
        "role": UserRole.SUPPORT,
    },
    {
        "email": "viewer@eventflow.local",
        "password": "password123",
        "full_name": "Viewer User",
        "role": UserRole.VIEWER,
    },
]


async def seed_users() -> None:
    async with AsyncSessionLocal() as session:
        for demo in DEMO_USERS:
            result = await session.execute(select(User).where(User.email == demo["email"]))
            existing = result.scalar_one_or_none()
            if existing:
                logger.info("User already exists: %s", demo["email"])
                continue

            user = User(
                email=demo["email"],
                hashed_password=hash_password(demo["password"]),
                full_name=demo["full_name"],
                role=demo["role"],
                is_active=True,
            )
            session.add(user)
            logger.info("Created user: %s (%s)", demo["email"], demo["role"].value)

        await session.commit()
    logger.info("Demo users seed complete")


def main() -> None:
    logging.basicConfig(level=logging.INFO)
    asyncio.run(seed_users())


if __name__ == "__main__":
    main()
