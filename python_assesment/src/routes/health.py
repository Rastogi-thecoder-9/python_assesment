from fastapi import APIRouter

from src.config.mongodb import database
from src.config.redis import redis_client

router = APIRouter()


@router.get("/health")
async def health_check():

    mongo_status = "healthy"
    redis_status = "healthy"

    try:
        await database.command("ping")
    except Exception:
        mongo_status = "unhealthy"

    try:
        await redis_client.ping()
    except Exception:
        redis_status = "unhealthy"

    return {
        "mongo": mongo_status,
        "redis": redis_status
    }