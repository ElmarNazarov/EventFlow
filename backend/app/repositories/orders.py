from datetime import datetime

from sqlalchemy import func, or_, select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

from app.core.constants import OrderStatus
from app.models.order import Order, OrderItem


class OrderRepository:
    def __init__(self, db: AsyncSession) -> None:
        self.db = db

    async def get_by_id(self, order_id: int) -> Order | None:
        result = await self.db.execute(
            select(Order)
            .options(selectinload(Order.items))
            .where(Order.id == order_id)
        )
        return result.scalar_one_or_none()

    async def get_by_order_number(self, order_number: str) -> Order | None:
        result = await self.db.execute(
            select(Order).where(Order.order_number == order_number)
        )
        return result.scalar_one_or_none()

    async def list_orders(
        self,
        *,
        offset: int,
        limit: int,
        status: OrderStatus | None = None,
        search: str | None = None,
        date_from: datetime | None = None,
        date_to: datetime | None = None,
        ordering: str = "-created_at",
    ) -> tuple[list[Order], int]:
        query = select(Order)
        count_query = select(func.count()).select_from(Order)

        if status:
            query = query.where(Order.status == status)
            count_query = count_query.where(Order.status == status)

        if search:
            pattern = f"%{search}%"
            search_filter = or_(
                Order.order_number.ilike(pattern),
                Order.customer_name.ilike(pattern),
                Order.customer_email.ilike(pattern),
            )
            query = query.where(search_filter)
            count_query = count_query.where(search_filter)

        if date_from:
            query = query.where(Order.created_at >= date_from)
            count_query = count_query.where(Order.created_at >= date_from)

        if date_to:
            query = query.where(Order.created_at <= date_to)
            count_query = count_query.where(Order.created_at <= date_to)

        order_column = Order.created_at
        if ordering.lstrip("-") == "created_at":
            order_column = Order.created_at.desc() if ordering.startswith("-") else Order.created_at.asc()
        elif ordering.lstrip("-") == "total_amount":
            order_column = (
                Order.total_amount.desc() if ordering.startswith("-") else Order.total_amount.asc()
            )

        query = query.order_by(order_column).offset(offset).limit(limit)

        total_result = await self.db.execute(count_query)
        total = total_result.scalar_one()

        result = await self.db.execute(query)
        return list(result.scalars().all()), total

    async def create(self, order: Order, items: list[OrderItem]) -> Order:
        self.db.add(order)
        await self.db.flush()
        for item in items:
            item.order_id = order.id
            self.db.add(item)
        await self.db.flush()
        await self.db.refresh(order, attribute_names=["items"])
        return order

    async def count_today(self) -> int:
        today = datetime.utcnow().date()
        result = await self.db.execute(
            select(func.count())
            .select_from(Order)
            .where(func.date(Order.created_at) == today)
        )
        return result.scalar_one()
