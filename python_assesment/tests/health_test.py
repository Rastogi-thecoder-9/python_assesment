async def test_health_endpoint(async_client):

    response = await async_client.get(
        "/health"
    )

    assert response.status_code == 200

    data = response.json()

    assert "mongo" in data
    assert "redis" in data

    assert data["mongo"] == "healthy"
    assert data["redis"] == "healthy"