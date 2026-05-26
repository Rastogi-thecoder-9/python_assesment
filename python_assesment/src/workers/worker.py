import asyncio
import random

from bson import ObjectId
from src.config.redis import redis_client
from src.config.mongodb import documents_collection
from src.settings.settings import settings
from src.services.rate_limit_service import decrement_active_jobs
from src.utils.object_id import validate_object_id
from src.constants import DOCUMENT_STATUSES, summary_cache_prefix


async def process_document(document_id: str):

    document = await documents_collection.find_one_and_update(
        {
            "_id": validate_object_id(document_id),
            "status": DOCUMENT_STATUSES.QUEUED
        },
        {
            "$set": {
                "status": DOCUMENT_STATUSES.PROCESSING
            }
        }
    )

    if not document:
        return

    user_id = document["user_id"]

    try:
        await asyncio.sleep(random.randint(10, 30))

        if random.random() < 0.1:
            raise Exception("Mock processing failure")

        summary = document["content"][:100]

        await documents_collection.update_one(
            {"_id": validate_object_id(document_id)},
            {
                "$set": {
                    "status": DOCUMENT_STATUSES.COMPLETED,
                    summary_cache_prefix: summary
                }
            }
        )

        cache_key = (
            f"{summary_cache_prefix}:{user_id}:{document['content_hash']}"
        )

        await redis_client.set(
            cache_key,
            summary,
            ex=settings.CACHE_TTL
        )

    except Exception:
        await documents_collection.update_one(
            {"_id": ObjectId(document_id)},
            {
                "$set": {
                    "status": DOCUMENT_STATUSES.FAILED
                }
            }
        )

    finally:
        await decrement_active_jobs(user_id)


async def worker_loop():

    while True:

        result = await redis_client.brpop(
            settings.QUEUE_NAME
        )

        _, document_id = result

        await process_document(document_id)


if __name__ == "__main__":
    asyncio.run(worker_loop())