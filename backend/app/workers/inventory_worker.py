import logging

from app.core.constants import QUEUE_RESERVE_INVENTORY
from app.core.database import AsyncSessionLocal
from app.messaging.commands import CommandMessage
from app.messaging.consumers import consume_queue
from app.messaging.producers import command_publisher
from app.services.inventory_service import InventoryService

logger = logging.getLogger(__name__)


async def handle_reserve_inventory(command: CommandMessage) -> None:
    async with AsyncSessionLocal() as session:
        service = InventoryService(session)
        success = await service.reserve_all_for_order(command.order_id)

    if success:
        logger.info("Inventory reserved for order %s", command.order_id)
        await command_publisher.publish_process_payment(command.order_id)
    else:
        logger.warning("Inventory reservation failed for order %s", command.order_id)
        await command_publisher.publish_send_notification(
            command.order_id,
            "INVENTORY_FAILED",
            f"Inventory reservation failed for order {command.order_id}",
        )


async def run_inventory_consumer() -> None:
    await consume_queue(QUEUE_RESERVE_INVENTORY, handle_reserve_inventory)
