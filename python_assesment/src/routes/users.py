from fastapi import APIRouter, Query

from src.config.mongodb import documents_collection

router = APIRouter()


@router.get("/users/{user_id}/documents")
async def list_user_documents(
    user_id: str,
    page: int = Query(1, ge=1),
    page_size: int = Query(10, ge=1, le=100),
    status: str | None = None
):

    query = {"user_id": user_id}

    if status:
        query["status"] = status

    skip = (page - 1) * page_size

    cursor = documents_collection.find(query)

    cursor = cursor.skip(skip).limit(page_size)

    documents = []

    async for doc in cursor:
        documents.append({
            "document_id": str(doc["_id"]),
            "title": doc["title"],
            "status": doc["status"]
        })

    return {
        "page": page,
        "page_size": page_size,
        "documents": documents
    }