import pytest

from bson import ObjectId

from src.workers.worker import process_document
from src.config.mongodb import documents_collection


@pytest.mark.asyncio
async def test_worker_processes_document():

    document = {
        "_id": ObjectId(),
        "user_id": "worker_user",
        "title": "Worker Test",
        "content": "Worker content",
        "content_hash": "hash123",
        "status": "queued",
        "summary": None
    }

    await documents_collection.insert_one(document)

    await process_document(
        str(document["_id"])
    )

    updated_document = await documents_collection.find_one({
        "_id": document["_id"]
    })

    assert updated_document["status"] in [
        "completed",
        "failed"
    ]


@pytest.mark.asyncio
async def test_worker_invalid_document():

    result = await process_document(
        "invalid_object_id"
    )

    assert result is None