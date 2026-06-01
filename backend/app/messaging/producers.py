from app.core.constants import (
    QUEUE_CREATE_SHIPPING,
    QUEUE_PROCESS_PAYMENT,
    QUEUE_RESERVE_INVENTORY,
    QUEUE_SEND_NOTIFICATION,
)
from app.messaging.commands import (
    CommandMessage,
    build_create_shipping_command,
    build_process_payment_command,
    build_reserve_inventory_command,
)
from app.messaging.rabbitmq import rabbitmq_client


class CommandPublisher:
    async def publish(self, queue_name: str, command: CommandMessage) -> None:
        await rabbitmq_client.publish_command(queue_name, command)

    async def publish_reserve_inventory(self, order_id: int, retry_count: int = 0) -> None:
        command = build_reserve_inventory_command(order_id, retry_count)
        await self.publish(QUEUE_RESERVE_INVENTORY, command)

    async def publish_process_payment(self, order_id: int, retry_count: int = 0) -> None:
        command = build_process_payment_command(order_id, retry_count)
        await self.publish(QUEUE_PROCESS_PAYMENT, command)

    async def publish_create_shipping(self, order_id: int, retry_count: int = 0) -> None:
        command = build_create_shipping_command(order_id, retry_count)
        await self.publish(QUEUE_CREATE_SHIPPING, command)

    async def publish_send_notification(
        self, order_id: int, notification_type: str, message: str
    ) -> None:
        from app.core.constants import CommandType

        command = CommandMessage(
            command_type=CommandType.SEND_NOTIFICATION,
            order_id=order_id,
            metadata={"notification_type": notification_type, "message": message},
        )
        await self.publish(QUEUE_SEND_NOTIFICATION, command)


command_publisher = CommandPublisher()
