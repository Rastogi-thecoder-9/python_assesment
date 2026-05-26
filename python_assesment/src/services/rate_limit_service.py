from fastapi import HTTPException

from src.config.redis import redis_client
from src.settings.settings import settings
from src.constants import active_jobs_key_prefix


async def check_rate_limit(user_id: str):
    key = f"{active_jobs_key_prefix}:{user_id}"

    count = await redis_client.get(key)
    count = int(count or 0)

    if count >= settings.MAX_ACTIVE_JOBS:
        raise HTTPException(
            status_code=429,
            detail="Too many active jobs"
        )


async def increment_active_jobs(user_id: str):
    key = f"{active_jobs_key_prefix}:{user_id}"

    await redis_client.incr(key)
    await redis_client.expire(key, 3600)


async def decrement_active_jobs(user_id: str):
    key = f"{active_jobs_key_prefix}:{user_id}"

    current = await redis_client.get(key)

    if current and int(current) > 0:
        await redis_client.decr(key)