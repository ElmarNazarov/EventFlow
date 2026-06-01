import logging

import aio_pika
from aio_pika.abc import AbstractChannel, AbstractRobustConnection

from app.core.config import get_settings

logger = logging.getLogger(__name__)


class RabbitMQClient:
    def __init__(self) -> None:
        self._connection: AbstractRobustConnection | None = None
        self._channel: AbstractChannel | None = None

    async def connect(self) -> None:
        settings = get_settings()
        self._connection = await aio_pika.connect_robust(settings.RABBITMQ_URL)
        self._channel = await self._connection.channel()
        logger.info("RabbitMQ connected")

    async def close(self) -> None:
        if self._connection and not self._connection.is_closed:
            await self._connection.close()
        self._connection = None
        self._channel = None
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


rabbitmq_client = RabbitMQClient()
