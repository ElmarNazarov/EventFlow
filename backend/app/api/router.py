from fastapi import APIRouter, Depends
from sqlalchemy import text
from sqlalchemy.ext.asyncio import AsyncSession

from app.api.deps import get_db
from app.core.config import get_settings
from app.core.redis import ping_redis
from app.messaging.kafka import kafka_client
from app.messaging.rabbitmq import rabbitmq_client

api_router = APIRouter()


@api_router.get("/health", tags=["health"])
async def health_check(db: AsyncSession = Depends(get_db)) -> dict:
    settings = get_settings()
    checks: dict[str, str] = {}

    try:
        await db.execute(text("SELECT 1"))
        checks["database"] = "ok"
    except Exception:
        checks["database"] = "error"

    checks["redis"] = "ok" if await ping_redis() else "error"

    try:
        checks["rabbitmq"] = "ok" if await rabbitmq_client.check_connection() else "error"
    except Exception:
        checks["rabbitmq"] = "not_configured"

    try:
        checks["kafka"] = "ok" if await kafka_client.check_connection() else "error"
    except Exception:
        checks["kafka"] = "not_configured"

    overall_status = "ok" if checks.get("database") == "ok" and checks.get("redis") == "ok" else "degraded"

    return {
        "status": overall_status,
        "app": settings.APP_NAME,
        "environment": settings.ENVIRONMENT,
        "checks": checks,
    }
