from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.shipping import Shipment


class ShipmentRepository:
    def __init__(self, db: AsyncSession) -> None:
        self.db = db

    async def get_by_order_id(self, order_id: int) -> Shipment | None:
        result = await self.db.execute(select(Shipment).where(Shipment.order_id == order_id))
        return result.scalar_one_or_none()

    async def create(self, shipment: Shipment) -> Shipment:
        self.db.add(shipment)
        await self.db.flush()
        await self.db.refresh(shipment)
        return shipment
