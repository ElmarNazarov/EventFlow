import logging

from app.core.constants import QUEUE_CREATE_SHIPPING
from app.core.database import AsyncSessionLocal
from app.messaging.commands import CommandMessage
from app.messaging.consumers import consume_queue
from app.services.shipping_service import ShippingService

logger = logging.getLogger(__name__)


async def handle_create_shipping(command: CommandMessage) -> None:
    async with AsyncSessionLocal() as session:
        service = ShippingService(session)
        success = await service.create_shipment_for_order(command.order_id)

    if success:
        logger.info("Shipment created for order %s", command.order_id)
    else:
        logger.warning("Shipping failed for order %s", command.order_id)


async def run_shipping_consumer() -> None:
    await consume_queue(QUEUE_CREATE_SHIPPING, handle_create_shipping)
