import logging

from app.core.constants import QUEUE_SEND_NOTIFICATION
from app.messaging.commands import CommandMessage
from app.messaging.consumers import consume_queue

logger = logging.getLogger(__name__)


async def handle_send_notification(command: CommandMessage) -> None:
    # Full notification persistence in Milestone 7
    logger.info(
        "Notification queued for order %s: %s — %s",
        command.order_id,
        command.metadata.get("notification_type"),
        command.metadata.get("message"),
    )


async def run_notification_consumer() -> None:
    await consume_queue(QUEUE_SEND_NOTIFICATION, handle_send_notification)
