from datetime import datetime, timezone
from bson import ObjectId

from src.config.mongodb import documents_collection
from src.utils.object_id import validate_object_id


async def create_document(document_data: dict):
    result = await documents_collection.insert_one(document_data)
    return str(result.inserted_id)


async def get_document(document_id: str):
    validated_id = validate_object_id(document_id)
    return await documents_collection.find_one({
        "_id": validated_id
    })


async def update_document(document_id: str, data: dict):
    validated_id = validate_object_id(document_id)
    data["updated_at"] = datetime.now(timezone.utc)

    await documents_collection.update_one(
        {"_id": validated_id},
        {"$set": data}
    )