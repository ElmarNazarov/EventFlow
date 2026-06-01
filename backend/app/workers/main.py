import asyncio
import logging
import signal

from app.core.config import get_settings
from app.core.logging import setup_logging
from app.messaging.rabbitmq import rabbitmq_client
from app.workers.inventory_worker import run_inventory_consumer
from app.workers.notification_worker import run_notification_consumer
from app.workers.payment_worker import run_payment_consumer
from app.workers.shipping_worker import run_shipping_consumer

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
            logger.warning("RabbitMQ connect attempt %s/30 failed: %s", attempt, exc)
            await asyncio.sleep(2)

    if not connected:
        logger.error("Failed to connect to RabbitMQ after retries")
        return

    logger.info("EventFlow workers started — consuming command queues")

    consumer_tasks = [
        asyncio.create_task(run_inventory_consumer()),
        asyncio.create_task(run_payment_consumer()),
        asyncio.create_task(run_shipping_consumer()),
        asyncio.create_task(run_notification_consumer()),
    ]

    await stop_event.wait()

    for task in consumer_tasks:
        task.cancel()
    await asyncio.gather(*consumer_tasks, return_exceptions=True)

    await rabbitmq_client.close()
    logger.info("EventFlow worker stopped")


def main() -> None:
    asyncio.run(run_worker())


if __name__ == "__main__":
    main()
