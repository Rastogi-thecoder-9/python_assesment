from motor.motor_asyncio import AsyncIOMotorDatabase
from redis.asyncio import Redis
from src.config.mongodb import database
from src.config.redis import redis_client


async def get_database() -> AsyncIOMotorDatabase:
    return database


async def get_redis() -> Redis:
    return redis_client