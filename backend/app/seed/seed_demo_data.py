"""Seed demo data for local development."""

import asyncio
import logging

from sqlalchemy import select

from app.core.constants import UserRole
from app.core.database import AsyncSessionLocal
from app.core.security import hash_password
from app.models.inventory import InventoryItem
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

DEMO_INVENTORY = [
    ("LAPTOP-PRO-14", "Laptop Pro 14\"", 45, 10),
    ("LAPTOP-AIR-13", "Laptop Air 13\"", 60, 15),
    ("MONITOR-27-4K", "Monitor 27\" 4K", 80, 20),
    ("KEYBOARD-MECH", "Mechanical Keyboard", 120, 25),
    ("MOUSE-WIRELESS", "Wireless Mouse", 200, 30),
    ("USB-C-HUB", "USB-C Hub", 150, 20),
    ("DOCK-STATION", "Docking Station", 70, 15),
    ("WEBCAM-HD", "HD Webcam", 90, 20),
    ("HEADSET-PRO", "Pro Headset", 55, 12),
    ("ROUTER-WIFI6", "WiFi 6 Router", 40, 10),
]


async def seed_users(session) -> None:
    for demo in DEMO_USERS:
        result = await session.execute(select(User).where(User.email == demo["email"]))
        if result.scalar_one_or_none():
            logger.info("User already exists: %s", demo["email"])
            continue
        session.add(
            User(
                email=demo["email"],
                hashed_password=hash_password(demo["password"]),
                full_name=demo["full_name"],
                role=demo["role"],
                is_active=True,
            )
        )
        logger.info("Created user: %s (%s)", demo["email"], demo["role"].value)


async def seed_inventory(session) -> None:
    for sku, name, qty, reorder in DEMO_INVENTORY:
        result = await session.execute(select(InventoryItem).where(InventoryItem.sku == sku))
        if result.scalar_one_or_none():
            logger.info("Inventory already exists: %s", sku)
            continue
        session.add(
            InventoryItem(
                sku=sku,
                name=name,
                available_quantity=qty,
                reserved_quantity=0,
                reorder_level=reorder,
                is_active=True,
            )
        )
        logger.info("Created inventory: %s", sku)


async def seed_all() -> None:
    async with AsyncSessionLocal() as session:
        await seed_users(session)
        await seed_inventory(session)
        await session.commit()
    logger.info("Demo seed complete")


def main() -> None:
    logging.basicConfig(level=logging.INFO)
    asyncio.run(seed_all())


if __name__ == "__main__":
    main()
