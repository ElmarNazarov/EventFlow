from fastapi import APIRouter, Depends
from sqlalchemy import text
from sqlalchemy.ext.asyncio import AsyncSession

from app.api.deps import get_db, require_mutation_role
from app.api.v1 import auth, inventory, orders, users
from app.core.config import get_settings
from app.core.redis import ping_redis
from app.messaging.kafka import kafka_client
from app.messaging.rabbitmq import rabbitmq_client
from app.models.user import User
from app.schemas.auth import MessageResponse

api_router = APIRouter()

api_router.include_router(auth.router)
api_router.include_router(users.router)
api_router.include_router(orders.router)
api_router.include_router(inventory.router)


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


@api_router.post("/protected/mutation-test", response_model=MessageResponse, tags=["auth"])
async def mutation_permission_test(
    _user: User = Depends(require_mutation_role),
) -> MessageResponse:
    """Placeholder endpoint to verify mutation-role RBAC (Milestone 2)."""
    return MessageResponse(message="Mutation allowed")
