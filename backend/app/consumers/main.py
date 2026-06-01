import asyncio
import logging
import signal

from app.core.config import get_settings
from app.core.logging import setup_logging
from app.messaging.kafka import kafka_client

logger = logging.getLogger(__name__)


async def run_consumer() -> None:
    setup_logging()
    settings = get_settings()
    logger.info("EventFlow event consumer starting (environment=%s)", settings.ENVIRONMENT)

    stop_event = asyncio.Event()

    def handle_shutdown() -> None:
        logger.info("Event consumer shutdown signal received")
        stop_event.set()

    loop = asyncio.get_running_loop()
    for sig in (signal.SIGTERM, signal.SIGINT):
        loop.add_signal_handler(sig, handle_shutdown)

    connected = False
    for attempt in range(1, 31):
        try:
            await kafka_client.connect()
            connected = True
            break
        except Exception as exc:
            logger.warning(
                "Kafka connect attempt %s/30 failed: %s",
                attempt,
                exc,
            )
            await asyncio.sleep(2)

    if not connected:
        logger.error("Failed to connect to Kafka after retries")
        return

    logger.info("EventFlow event consumer started — waiting for events (Milestone 5)")

    try:
        while not stop_event.is_set():
            await asyncio.sleep(5)
            logger.debug("Event consumer heartbeat")
    finally:
        await kafka_client.close()
        logger.info("EventFlow event consumer stopped")


def main() -> None:
    asyncio.run(run_consumer())


if __name__ == "__main__":
    main()
