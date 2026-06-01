import asyncio
import logging
import signal

from app.core.config import get_settings
from app.core.logging import setup_logging
from app.messaging.rabbitmq import rabbitmq_client

logger = logging.getLogger(__name__)


async def run_worker() -> None:
    setup_logging()
    settings = get_settings()
    logger.info("EventFlow worker starting (environment=%s)", settings.ENVIRONMENT)

    stop_event = asyncio.Event()

    def handle_shutdown() -> None:
        logger.info("Worker shutdown signal received")
        stop_event.set()

    loop = asyncio.get_running_loop()
    for sig in (signal.SIGTERM, signal.SIGINT):
        loop.add_signal_handler(sig, handle_shutdown)

    connected = False
    for attempt in range(1, 31):
        try:
            await rabbitmq_client.connect()
            connected = True
            break
        except Exception as exc:
            logger.warning(
                "RabbitMQ connect attempt %s/30 failed: %s",
                attempt,
                exc,
            )
            await asyncio.sleep(2)

    if not connected:
        logger.error("Failed to connect to RabbitMQ after retries")
        return

    logger.info("EventFlow worker started — waiting for commands (Milestone 4)")

    try:
        while not stop_event.is_set():
            await asyncio.sleep(5)
            logger.debug("Worker heartbeat")
    finally:
        await rabbitmq_client.close()
        logger.info("EventFlow worker stopped")


def main() -> None:
    asyncio.run(run_worker())


if __name__ == "__main__":
    main()
