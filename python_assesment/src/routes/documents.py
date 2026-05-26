from fastapi import APIRouter, HTTPException
from datetime import datetime, timezone

from src.constants import DOCUMENT_STATUSES, summary_cache_prefix
from src.schemas.document import (
    DocumentCreate,
    DocumentResponse,
    DocumentStatusResponse
)

from src.services.cache_service import generate_content_hash
from src.services.document_service import (
    create_document,
    get_document
)

from src.services.queue_service import enqueue_document

from src.services.rate_limit_service import (
    check_rate_limit,
    increment_active_jobs
)

from src.config.redis import redis_client
from src.settings.settings import settings

router = APIRouter()


@router.post("/documents", response_model=DocumentResponse)
async def submit_document(payload: DocumentCreate):

    await check_rate_limit(payload.user_id)

    content_hash = generate_content_hash(payload.content)

    cache_key = f"{summary_cache_prefix}:{payload.user_id}:{content_hash}"

    cached = await redis_client.get(cache_key)

    if cached:
        return {
            "document_id": "cached",
            "status": DOCUMENT_STATUSES.COMPLETED
            
        }

    document = {
        "user_id": payload.user_id,
        "title": payload.title,
        "content": payload.content,
        "content_hash": content_hash,
        "status": DOCUMENT_STATUSES.QUEUED,
        summary_cache_prefix: None,
        "created_at": datetime.now(timezone.utc),
        "updated_at": datetime.now(timezone.utc)
    }

    document_id = await create_document(document)

    await increment_active_jobs(payload.user_id)

    await enqueue_document(document_id)

    return {
        "document_id": document_id,
        "status": DOCUMENT_STATUSES.QUEUED
    }


@router.get("/documents/{document_id}")
async def get_document_status(document_id: str):

    document = await get_document(document_id)

    if not document:
        raise HTTPException(
            status_code=404,
            detail="Document not found"
        )

    return {
        "document_id": str(document["_id"]),
        "status": document["status"],
        summary_cache_prefix: document.get(summary_cache_prefix)
    }