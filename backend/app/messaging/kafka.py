import logging

from aiokafka import AIOKafkaProducer

from app.core.config import get_settings

logger = logging.getLogger(__name__)


class KafkaClient:
    def __init__(self) -> None:
        self._producer: AIOKafkaProducer | None = None

    async def connect(self) -> None:
        settings = get_settings()
        self._producer = AIOKafkaProducer(
            bootstrap_servers=settings.KAFKA_BOOTSTRAP_SERVERS,
        )
        await self._producer.start()
        logger.info("Kafka producer connected")

    async def close(self) -> None:
        if self._producer is not None:
            await self._producer.stop()
            self._producer = None
        logger.info("Kafka producer closed")

    async def check_connection(self) -> bool:
        producer = None
        try:
            settings = get_settings()
            producer = AIOKafkaProducer(
                bootstrap_servers=settings.KAFKA_BOOTSTRAP_SERVERS,
            )
            await producer.start()
            await producer.client.fetch_all_metadata()
            return True
        except Exception as exc:
            logger.debug("Kafka health check failed: %s", exc)
            return False
        finally:
            if producer is not None:
                await producer.stop()


kafka_client = KafkaClient()
