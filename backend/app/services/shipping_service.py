import uuid

from sqlalchemy.ext.asyncio import AsyncSession

from app.core.constants import OrderStatus, ShipmentStatus
from app.models.shipping import Shipment
from app.repositories.orders import OrderRepository
from app.repositories.shipping import ShipmentRepository


class ShippingService:
    def __init__(self, db: AsyncSession) -> None:
        self.db = db
        self.orders = OrderRepository(db)
        self.shipments = ShipmentRepository(db)

    async def create_shipment_for_order(self, order_id: int) -> bool:
        order = await self.orders.get_by_id(order_id)
        if order is None:
            return False

        if order.status == OrderStatus.COMPLETED:
            return True

        if order.status not in (
            OrderStatus.PAYMENT_CONFIRMED,
            OrderStatus.SHIPPING_PENDING,
        ):
            return False

        existing = await self.shipments.get_by_order_id(order_id)
        if existing and existing.status == ShipmentStatus.SHIPPED:
            await self.orders.update_status(order, OrderStatus.COMPLETED)
            await self.db.commit()
            return True

        tracking = f"EF-{uuid.uuid4().hex[:10].upper()}"
        shipment = existing or Shipment(
            order_id=order_id,
            status=ShipmentStatus.PENDING,
            carrier="EventFlow Logistics",
            shipping_address=f"Ship to: {order.customer_name}",
        )
        if existing is None:
            shipment = await self.shipments.create(shipment)

        shipment.tracking_number = tracking
        shipment.status = ShipmentStatus.SHIPPED

        await self.orders.update_status(order, OrderStatus.SHIPPED)
        await self.db.commit()

        await self.orders.update_status(order, OrderStatus.COMPLETED)
        await self.db.commit()
        return True
