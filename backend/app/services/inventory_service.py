from sqlalchemy.ext.asyncio import AsyncSession

from app.core.constants import ReservationStatus
from app.core.exceptions import AppException
from app.core.pagination import PaginatedResponse, PaginationParams
from app.models.inventory import InventoryItem, InventoryReservation
from app.core.constants import OrderStatus
from app.repositories.inventory import InventoryRepository
from app.repositories.orders import OrderRepository
from app.schemas.inventory import (
    InventoryItemCreate,
    InventoryItemRead,
    InventoryItemUpdate,
    InventoryReservationRead,
)


class InventoryService:
    def __init__(self, db: AsyncSession) -> None:
        self.db = db
        self.inventory = InventoryRepository(db)
        self.orders = OrderRepository(db)

    async def list_items(
        self,
        pagination: PaginationParams,
        *,
        search: str | None = None,
        active_only: bool = False,
    ) -> PaginatedResponse[InventoryItemRead]:
        items, total = await self.inventory.list_items(
            offset=pagination.offset,
            limit=pagination.page_size,
            search=search,
            active_only=active_only,
        )
        pages = (total + pagination.page_size - 1) // pagination.page_size if total else 0
        return PaginatedResponse(
            items=[InventoryItemRead.model_validate(i) for i in items],
            total=total,
            page=pagination.page,
            page_size=pagination.page_size,
            pages=pages,
        )

    async def create_item(self, data: InventoryItemCreate) -> InventoryItemRead:
        existing = await self.inventory.get_by_sku(data.sku)
        if existing:
            raise AppException(f"SKU already exists: {data.sku}", status_code=400)

        item = InventoryItem(
            sku=data.sku.upper(),
            name=data.name,
            available_quantity=data.available_quantity,
            reserved_quantity=0,
            reorder_level=data.reorder_level,
            is_active=data.is_active,
        )
        created = await self.inventory.create(item)
        await self.db.commit()
        return InventoryItemRead.model_validate(created)

    async def update_item(
        self, inventory_id: int, data: InventoryItemUpdate
    ) -> InventoryItemRead:
        item = await self.inventory.get_by_id(inventory_id)
        if item is None:
            raise AppException("Inventory item not found", status_code=404)

        if data.name is not None:
            item.name = data.name
        if data.available_quantity is not None:
            item.available_quantity = data.available_quantity
        if data.reorder_level is not None:
            item.reorder_level = data.reorder_level
        if data.is_active is not None:
            item.is_active = data.is_active

        updated = await self.inventory.update(item)
        await self.db.commit()
        return InventoryItemRead.model_validate(updated)

    async def reserve_inventory(
        self, order_id: int, sku: str, quantity: int
    ) -> InventoryReservationRead:
        """Reserve stock for an order line. Used by workers in Milestone 4."""
        item = await self.inventory.get_by_sku(sku)
        if item is None:
            raise AppException(f"SKU not found: {sku}", status_code=404)

        if item.available_quantity < quantity:
            reservation = InventoryReservation(
                order_id=order_id,
                sku=item.sku,
                quantity=quantity,
                status=ReservationStatus.FAILED,
            )
            created = await self.inventory.create_reservation(reservation)
            await self.db.commit()
            return InventoryReservationRead.model_validate(created)

        item.available_quantity -= quantity
        item.reserved_quantity += quantity

        reservation = InventoryReservation(
            order_id=order_id,
            sku=item.sku,
            quantity=quantity,
            status=ReservationStatus.RESERVED,
        )
        created = await self.inventory.create_reservation(reservation)
        await self.inventory.update(item)
        await self.db.commit()
        return InventoryReservationRead.model_validate(created)

    async def reserve_all_for_order(self, order_id: int) -> bool:
        """Reserve inventory for all order lines. Returns False if any line fails."""
        order = await self.orders.get_by_id(order_id)
        if order is None:
            return False

        if order.status not in (
            OrderStatus.CREATED,
            OrderStatus.INVENTORY_PENDING,
        ):
            # Already processed or terminal state
            return order.status in (
                OrderStatus.INVENTORY_RESERVED,
                OrderStatus.PAYMENT_PENDING,
                OrderStatus.PAYMENT_CONFIRMED,
                OrderStatus.SHIPPING_PENDING,
                OrderStatus.SHIPPED,
                OrderStatus.COMPLETED,
            )

        reserved_lines: list[tuple[str, int]] = []
        for item in order.items:
            item_db = await self.inventory.get_by_sku(item.sku)
            if item_db is None or item_db.available_quantity < item.quantity:
                for sku, qty in reserved_lines:
                    await self._release_line(order_id, sku, qty)
                reservation = InventoryReservation(
                    order_id=order_id,
                    sku=item.sku,
                    quantity=item.quantity,
                    status=ReservationStatus.FAILED,
                )
                self.db.add(reservation)
                await self.orders.update_status(order, OrderStatus.FAILED)
                await self.db.commit()
                return False

            item_db.available_quantity -= item.quantity
            item_db.reserved_quantity += item.quantity
            await self.inventory.update(item_db)
            reservation = InventoryReservation(
                order_id=order_id,
                sku=item.sku,
                quantity=item.quantity,
                status=ReservationStatus.RESERVED,
            )
            self.db.add(reservation)
            reserved_lines.append((item.sku, item.quantity))

        await self.orders.update_status(order, OrderStatus.INVENTORY_RESERVED)
        await self.db.commit()
        return True

    async def _release_line(self, order_id: int, sku: str, quantity: int) -> None:
        item = await self.inventory.get_by_sku(sku)
        if item:
            item.available_quantity += quantity
            item.reserved_quantity = max(0, item.reserved_quantity - quantity)
            await self.inventory.update(item)

    async def release_inventory(self, order_id: int) -> None:
        """Release reserved stock when an order is cancelled."""
        reservations = await self.inventory.get_reservations_for_order(order_id)
        for res in reservations:
            if res.status != ReservationStatus.RESERVED:
                continue
            item = await self.inventory.get_by_sku(res.sku)
            if item:
                item.available_quantity += res.quantity
                item.reserved_quantity = max(0, item.reserved_quantity - res.quantity)
                await self.inventory.update(item)
            res.status = ReservationStatus.RELEASED
        await self.db.commit()
