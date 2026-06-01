from sqlalchemy import func, or_, select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.inventory import InventoryItem, InventoryReservation
from app.core.constants import ReservationStatus


class InventoryRepository:
    def __init__(self, db: AsyncSession) -> None:
        self.db = db

    async def get_by_id(self, inventory_id: int) -> InventoryItem | None:
        result = await self.db.execute(
            select(InventoryItem).where(InventoryItem.id == inventory_id)
        )
        return result.scalar_one_or_none()

    async def get_by_sku(self, sku: str) -> InventoryItem | None:
        result = await self.db.execute(
            select(InventoryItem).where(InventoryItem.sku == sku.upper())
        )
        return result.scalar_one_or_none()

    async def get_by_skus(self, skus: list[str]) -> list[InventoryItem]:
        upper_skus = [s.upper() for s in skus]
        result = await self.db.execute(
            select(InventoryItem).where(InventoryItem.sku.in_(upper_skus))
        )
        return list(result.scalars().all())

    async def list_items(
        self,
        *,
        offset: int,
        limit: int,
        search: str | None = None,
        active_only: bool = False,
    ) -> tuple[list[InventoryItem], int]:
        query = select(InventoryItem)
        count_query = select(func.count()).select_from(InventoryItem)

        if search:
            pattern = f"%{search}%"
            search_filter = or_(
                InventoryItem.sku.ilike(pattern),
                InventoryItem.name.ilike(pattern),
            )
            query = query.where(search_filter)
            count_query = count_query.where(search_filter)

        if active_only:
            query = query.where(InventoryItem.is_active.is_(True))
            count_query = count_query.where(InventoryItem.is_active.is_(True))

        query = query.order_by(InventoryItem.sku).offset(offset).limit(limit)

        total_result = await self.db.execute(count_query)
        total = total_result.scalar_one()

        result = await self.db.execute(query)
        return list(result.scalars().all()), total

    async def create(self, item: InventoryItem) -> InventoryItem:
        self.db.add(item)
        await self.db.flush()
        await self.db.refresh(item)
        return item

    async def update(self, item: InventoryItem) -> InventoryItem:
        await self.db.flush()
        await self.db.refresh(item)
        return item

    async def create_reservation(self, reservation: InventoryReservation) -> InventoryReservation:
        self.db.add(reservation)
        await self.db.flush()
        await self.db.refresh(reservation)
        return reservation

    async def get_reservations_for_order(self, order_id: int) -> list[InventoryReservation]:
        result = await self.db.execute(
            select(InventoryReservation).where(InventoryReservation.order_id == order_id)
        )
        return list(result.scalars().all())
