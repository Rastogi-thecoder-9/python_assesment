import pytest_asyncio

from httpx import AsyncClient
from motor.motor_asyncio import AsyncIOMotorClient

from src.main import app
from src.config.mongodb import documents_collection
from src.config.redis import redis_client


TEST_MONGO_URL = "mongodb://localhost:27017"
TEST_DB_NAME = "test_document_db"


@pytest_asyncio.fixture(scope="session")
async def mongo_client():
    client = AsyncIOMotorClient(TEST_MONGO_URL)

    yield client

    client.close()


@pytest_asyncio.fixture(autouse=True)
async def clear_database():

    await documents_collection.delete_many({})

    await redis_client.flushdb()

    yield

    await documents_collection.delete_many({})

    await redis_client.flushdb()


@pytest_asyncio.fixture
async def async_client():

    async with AsyncClient(
        app=app,
        base_url="http://test"
    ) as client:

        yield client