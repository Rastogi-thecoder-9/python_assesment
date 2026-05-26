from src.config.redis import redis_client
from src.settings.settings import settings


async def enqueue_document(document_id: str):
    await redis_client.lpush(
        settings.QUEUE_NAME,
        document_id
    )