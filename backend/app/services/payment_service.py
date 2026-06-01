import uuid
from datetime import UTC, datetime
from decimal import Decimal

from sqlalchemy.ext.asyncio import AsyncSession

from app.core.constants import (
    PAYMENT_FAILURE_THRESHOLD,
    OrderStatus,
    PaymentStatus,
)
from app.messaging.producers import command_publisher
from app.models.payment import Payment
from app.repositories.orders import OrderRepository
from app.repositories.payments import PaymentRepository


class PaymentService:
    def __init__(self, db: AsyncSession) -> None:
        self.db = db
        self.orders = OrderRepository(db)
        self.payments = PaymentRepository(db)

    def _should_fail_payment(self, amount: Decimal) -> bool:
        return amount > PAYMENT_FAILURE_THRESHOLD

    async def process_payment_for_order(self, order_id: int) -> bool:
        order = await self.orders.get_by_id(order_id)
        if order is None:
            return False

        if order.status in (OrderStatus.COMPLETED, OrderStatus.CANCELLED, OrderStatus.FAILED):
            return order.status == OrderStatus.COMPLETED

        existing = await self.payments.get_by_order_id(order_id)
        if existing and existing.status == PaymentStatus.CONFIRMED:
            return True

        if order.status not in (
            OrderStatus.INVENTORY_RESERVED,
            OrderStatus.PAYMENT_PENDING,
        ):
            if order.status == OrderStatus.PAYMENT_CONFIRMED:
                return True
            return False

        await self.orders.update_status(order, OrderStatus.PAYMENT_PENDING)

        payment = existing or Payment(
            order_id=order_id,
            amount=order.total_amount,
            currency=order.currency,
            status=PaymentStatus.PENDING,
            provider="simulated",
        )
        if existing is None:
            payment = await self.payments.create(payment)

        if self._should_fail_payment(order.total_amount):
            payment.status = PaymentStatus.FAILED
            payment.failure_reason = (
                f"Simulated decline: amount exceeds {PAYMENT_FAILURE_THRESHOLD}"
            )
            payment.processed_at = datetime.now(UTC)
            await self.orders.update_status(order, OrderStatus.PAYMENT_FAILED)
            await self.db.commit()
            await command_publisher.publish_send_notification(
                order_id,
                "PAYMENT_FAILED",
                f"Payment failed for order {order.order_number}",
            )
            return False

        payment.status = PaymentStatus.CONFIRMED
        payment.provider_reference = f"SIM-{uuid.uuid4().hex[:12].upper()}"
        payment.processed_at = datetime.now(UTC)
        await self.orders.update_status(order, OrderStatus.PAYMENT_CONFIRMED)
        await self.db.commit()

        await self.orders.update_status(order, OrderStatus.SHIPPING_PENDING)
        await self.db.commit()

        await command_publisher.publish_create_shipping(order_id)
        return True
