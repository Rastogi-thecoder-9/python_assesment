from src.config.redis import redis_client
from src.services.cache_service import generate_content_hash


async def test_duplicate_content_cache(async_client):

    payload = {
        "user_id": "cache_user",
        "title": "Cache Test",
        "content": "Duplicate document content"
    }

    response_1 = await async_client.post(
        "/documents",
        json=payload
    )

    assert response_1.status_code == 200

    content_hash = generate_content_hash(
        payload["content"]
    )

    cache_key = (
        f"summary:{payload['user_id']}:{content_hash}"
    )

    await redis_client.set(
        cache_key,
        "Cached Summary"
    )

    response_2 = await async_client.post(
        "/documents",
        json=payload
    )

    assert response_2.status_code == 200

    data = response_2.json()

    assert data["status"] == "completed"