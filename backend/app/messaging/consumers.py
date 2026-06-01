import logging
from collections.abc import Awaitable, Callable

import aio_pika
from aio_pika.abc import AbstractIncomingMessage

from app.core.idempotency import is_command_processed, mark_command_processed
from app.messaging.commands import CommandMessage
from app.messaging.rabbitmq import rabbitmq_client

logger = logging.getLogger(__name__)

CommandHandler = Callable[[CommandMessage], Awaitable[None]]


async def consume_queue(queue_name: str, handler: CommandHandler) -> None:
    channel = await rabbitmq_client.get_channel()
    queue = await channel.declare_queue(queue_name, durable=True)

    async def on_message(message: AbstractIncomingMessage) -> None:
        async with message.process(requeue=False):
            try:
                command = CommandMessage.from_json(message.body)
                if await is_command_processed(command.command_id):
                    logger.info("Skipping duplicate command %s", command.command_id)
                    return
                await handler(command)
                await mark_command_processed(command.command_id)
            except Exception:
                logger.exception("Error processing message on queue %s", queue_name)
                raise

    await queue.consume(on_message)
    logger.info("Consuming queue: %s", queue_name)
