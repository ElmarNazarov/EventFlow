import logging

import aio_pika
from aio_pika import DeliveryMode, Message
from aio_pika.abc import AbstractChannel, AbstractRobustConnection

from app.core.config import get_settings
from app.core.constants import (
    QUEUE_CREATE_SHIPPING,
    QUEUE_PROCESS_PAYMENT,
    QUEUE_RESERVE_INVENTORY,
    QUEUE_SEND_NOTIFICATION,
)
from app.messaging.commands import CommandMessage

logger = logging.getLogger(__name__)

COMMAND_QUEUES = (
    QUEUE_RESERVE_INVENTORY,
    QUEUE_PROCESS_PAYMENT,
    QUEUE_CREATE_SHIPPING,
    QUEUE_SEND_NOTIFICATION,
)


class RabbitMQClient:
    def __init__(self) -> None:
        self._connection: AbstractRobustConnection | None = None
        self._channel: AbstractChannel | None = None
        self._queues_declared = False

    async def connect(self) -> None:
        settings = get_settings()
        self._connection = await aio_pika.connect_robust(settings.RABBITMQ_URL)
        self._channel = await self._connection.channel()
        await self._channel.set_qos(prefetch_count=1)
        await self.declare_queues()
        logger.info("RabbitMQ connected")

    async def declare_queues(self) -> None:
        if self._queues_declared and self._channel and not self._channel.is_closed:
            return
        channel = await self.get_channel()
        for queue_name in COMMAND_QUEUES:
            await channel.declare_queue(queue_name, durable=True)
        self._queues_declared = True
        logger.debug("RabbitMQ command queues declared")

    async def close(self) -> None:
        if self._connection and not self._connection.is_closed:
            await self._connection.close()
        self._connection = None
        self._channel = None
        self._queues_declared = False
        logger.info("RabbitMQ connection closed")

    async def check_connection(self) -> bool:
        try:
            settings = get_settings()
            connection = await aio_pika.connect_robust(settings.RABBITMQ_URL)
            await connection.close()
            return True
        except Exception as exc:
            logger.debug("RabbitMQ health check failed: %s", exc)
            return False

    async def get_channel(self) -> AbstractChannel:
        if self._channel is None or self._channel.is_closed:
            await self.connect()
        assert self._channel is not None
        return self._channel

    async def publish_command(self, queue_name: str, command: CommandMessage) -> None:
        channel = await self.get_channel()
        await channel.declare_queue(queue_name, durable=True)
        message = Message(
            body=command.to_json(),
            delivery_mode=DeliveryMode.PERSISTENT,
            content_type="application/json",
        )
        await channel.default_exchange.publish(message, routing_key=queue_name)
        logger.info(
            "Published command %s for order %s to queue %s",
            command.command_id,
            command.order_id,
            queue_name,
        )


rabbitmq_client = RabbitMQClient()
