from unittest.mock import patch


async def test_redis_failure(async_client):

    payload = {
        "user_id": "redis_fail",
        "title": "Redis Failure",
        "content": "Redis failure test content"
    }

    with patch(
        "app.db.redis.redis_client.get"
    ) as mock_get:

        mock_get.side_effect = Exception(
            "Redis unavailable"
        )

        response = await async_client.post(
            "/documents",
            json=payload
        )

        assert response.status_code in [200, 500]


async def test_mongo_failure(async_client):

    with patch(
        "app.db.mongodb.documents_collection.insert_one"
    ) as mock_insert:

        mock_insert.side_effect = Exception(
            "Mongo unavailable"
        )

        payload = {
            "user_id": "mongo_fail",
            "title": "Mongo Failure",
            "content": "Mongo failure test content"
        }

        response = await async_client.post(
            "/documents",
            json=payload
        )

        assert response.status_code == 500