import logging

from app.core.redis import get_redis

logger = logging.getLogger(__name__)

COMMAND_KEY_PREFIX = "eventflow:command:"
COMMAND_TTL_SECONDS = 60 * 60 * 24  # 24 hours


async def is_command_processed(command_id: str) -> bool:
    try:
        redis = await get_redis()
        return await redis.exists(f"{COMMAND_KEY_PREFIX}{command_id}") == 1
    except Exception as exc:
        logger.warning("Idempotency check failed, allowing processing: %s", exc)
        return False


async def mark_command_processed(command_id: str) -> None:
    try:
        redis = await get_redis()
        await redis.setex(f"{COMMAND_KEY_PREFIX}{command_id}", COMMAND_TTL_SECONDS, "1")
    except Exception as exc:
        logger.warning("Failed to mark command processed: %s", exc)
