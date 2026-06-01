from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.payment import Payment


class PaymentRepository:
    def __init__(self, db: AsyncSession) -> None:
        self.db = db

    async def get_by_order_id(self, order_id: int) -> Payment | None:
        result = await self.db.execute(select(Payment).where(Payment.order_id == order_id))
        return result.scalar_one_or_none()

    async def create(self, payment: Payment) -> Payment:
        self.db.add(payment)
        await self.db.flush()
        await self.db.refresh(payment)
        return payment
