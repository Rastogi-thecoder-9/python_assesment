from motor.motor_asyncio import AsyncIOMotorClient
from src.settings.settings import settings

client = AsyncIOMotorClient(settings.MONGO_URL)
database = client[settings.DATABASE_NAME]

documents_collection = database.documents

async def create_indexes():

    await documents_collection.create_index(
        [
            ("user_id", 1),
            ("status", 1)
        ],
        name="idx_user_status"
    )

    await documents_collection.create_index(
        "content_hash",
        name="idx_content_hash"
    )