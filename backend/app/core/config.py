from functools import lru_cache

from pydantic import field_validator
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        case_sensitive=False,
        extra="ignore",
    )

    APP_NAME: str = "EventFlow"
    ENVIRONMENT: str = "local"
    DEBUG: bool = True
    SECRET_KEY: str = "change-me"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 60

    DATABASE_URL: str = "postgresql+asyncpg://eventflow:eventflow@db:5432/eventflow"
    SYNC_DATABASE_URL: str = "postgresql://eventflow:eventflow@db:5432/eventflow"

    REDIS_URL: str = "redis://redis:6379/0"
    RABBITMQ_URL: str = "amqp://guest:guest@rabbitmq:5672/"

    KAFKA_BOOTSTRAP_SERVERS: str = "kafka:9092"
    KAFKA_ORDER_EVENTS_TOPIC: str = "order-events"
    KAFKA_INVENTORY_EVENTS_TOPIC: str = "inventory-events"
    KAFKA_PAYMENT_EVENTS_TOPIC: str = "payment-events"
    KAFKA_SHIPPING_EVENTS_TOPIC: str = "shipping-events"
    KAFKA_WORKFLOW_EVENTS_TOPIC: str = "workflow-events"
    KAFKA_NOTIFICATION_EVENTS_TOPIC: str = "notification-events"

    CORS_ORIGINS: str = "http://localhost:3000"

    @field_validator("CORS_ORIGINS", mode="before")
    @classmethod
    def parse_cors_origins(cls, value: str | list[str]) -> str:
        if isinstance(value, list):
            return ",".join(value)
        return value

    @property
    def cors_origins_list(self) -> list[str]:
        return [origin.strip() for origin in self.CORS_ORIGINS.split(",") if origin.strip()]


@lru_cache
def get_settings() -> Settings:
    return Settings()
