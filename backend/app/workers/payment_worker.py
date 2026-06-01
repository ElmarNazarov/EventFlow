import logging

from app.core.constants import QUEUE_PROCESS_PAYMENT
from app.core.database import AsyncSessionLocal
from app.messaging.commands import CommandMessage
from app.messaging.consumers import consume_queue
from app.services.payment_service import PaymentService

logger = logging.getLogger(__name__)


async def handle_process_payment(command: CommandMessage) -> None:
    async with AsyncSessionLocal() as session:
        service = PaymentService(session)
        success = await service.process_payment_for_order(command.order_id)

    if success:
        logger.info("Payment processed for order %s", command.order_id)
    else:
        logger.warning("Payment failed for order %s", command.order_id)


async def run_payment_consumer() -> None:
    await consume_queue(QUEUE_PROCESS_PAYMENT, handle_process_payment)
