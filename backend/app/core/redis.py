import redis.asyncio as aioredis

from app.core.config import get_settings

settings = get_settings()

_redis_client: aioredis.Redis | None = None


async def get_redis() -> aioredis.Redis:
    global _redis_client
    if _redis_client is None:
        _redis_client = aioredis.from_url(
            settings.REDIS_URL,
            encoding="utf-8",
            decode_responses=True,
        )
    return _redis_client


async def ping_redis() -> bool:
    try:
        client = await get_redis()
        return await client.ping()
    except Exception:
        return False


async def close_redis() -> None:
    global _redis_client
    if _redis_client is not None:
        await _redis_client.aclose()
        _redis_client = None
