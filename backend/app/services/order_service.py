import uuid
from datetime import datetime
from decimal import Decimal

from sqlalchemy.ext.asyncio import AsyncSession

from app.core.constants import OrderStatus
from app.core.exceptions import AppException
from app.core.pagination import PaginatedResponse, PaginationParams
from app.models.order import Order, OrderItem
from app.models.user import User
from app.messaging.producers import command_publisher
from app.repositories.inventory import InventoryRepository
from app.repositories.orders import OrderRepository
from app.schemas.order import OrderCreate, OrderListItem, OrderRead


class OrderService:
    def __init__(self, db: AsyncSession) -> None:
        self.db = db
        self.orders = OrderRepository(db)
        self.inventory = InventoryRepository(db)

    def _generate_order_number(self) -> str:
        date_part = datetime.utcnow().strftime("%Y%m%d")
        unique = uuid.uuid4().hex[:6].upper()
        return f"ORD-{date_part}-{unique}"

    async def create_order(self, data: OrderCreate, created_by: User) -> OrderRead:
        skus = [item.sku for item in data.items]
        inventory_items = await self.inventory.get_by_skus(skus)
        inventory_map = {i.sku: i for i in inventory_items}

        missing = [sku for sku in skus if sku.upper() not in inventory_map]
        if missing:
            raise AppException(f"Unknown SKU(s): {', '.join(missing)}", status_code=400)

        inactive = [sku for sku, inv in inventory_map.items() if not inv.is_active]
        if inactive:
            raise AppException(f"Inactive SKU(s): {', '.join(inactive)}", status_code=400)

        order_items: list[OrderItem] = []
        total = Decimal("0")

        for line in data.items:
            inv = inventory_map[line.sku.upper()]
            unit_price = line.unit_price if line.unit_price is not None else Decimal("99.99")
            line_total = unit_price * line.quantity
            total += line_total
            order_items.append(
                OrderItem(
                    sku=inv.sku,
                    product_name=inv.name,
                    quantity=line.quantity,
                    unit_price=unit_price,
                    total_price=line_total,
                )
            )

        order = Order(
            order_number=self._generate_order_number(),
            customer_name=data.customer_name,
            customer_email=data.customer_email,
            status=OrderStatus.CREATED,
            total_amount=total,
            currency=data.currency,
            created_by_id=created_by.id,
        )

        created = await self.orders.create(order, order_items)
        await self.orders.update_status(created, OrderStatus.INVENTORY_PENDING)
        await self.db.commit()

        await command_publisher.publish_reserve_inventory(created.id)

        refreshed = await self.orders.get_by_id(created.id)
        if refreshed is None:
            raise AppException("Failed to create order", status_code=500)
        return OrderRead.model_validate(refreshed)

    async def get_order(self, order_id: int) -> OrderRead:
        order = await self.orders.get_by_id(order_id)
        if order is None:
            raise AppException("Order not found", status_code=404)
        return OrderRead.model_validate(order)

    async def list_orders(
        self,
        pagination: PaginationParams,
        *,
        status: OrderStatus | None = None,
        search: str | None = None,
        date_from: datetime | None = None,
        date_to: datetime | None = None,
        ordering: str = "-created_at",
    ) -> PaginatedResponse[OrderListItem]:
        orders, total = await self.orders.list_orders(
            offset=pagination.offset,
            limit=pagination.page_size,
            status=status,
            search=search,
            date_from=date_from,
            date_to=date_to,
            ordering=ordering,
        )
        pages = (total + pagination.page_size - 1) // pagination.page_size if total else 0
        return PaginatedResponse(
            items=[OrderListItem.model_validate(o) for o in orders],
            total=total,
            page=pagination.page,
            page_size=pagination.page_size,
            pages=pages,
        )
