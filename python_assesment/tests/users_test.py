async def test_list_user_documents(async_client):

    payload = {
        "user_id": "list_user",
        "title": "Test",
        "content": "Valid content for listing"
    }

    for _ in range(5):

        await async_client.post(
            "/documents",
            json=payload
        )

    response = await async_client.get(
        "/users/list_user/documents?page=1&page_size=2"
    )

    assert response.status_code == 200

    data = response.json()

    assert data["page"] == 1
    assert data["page_size"] == 2

    assert len(data["documents"]) == 2


async def test_filter_user_documents(async_client):

    payload = {
        "user_id": "filter_user",
        "title": "Filter Test",
        "content": "Filter content"
    }

    await async_client.post(
        "/documents",
        json=payload
    )

    response = await async_client.get(
        "/users/filter_user/documents?status=queued"
    )

    assert response.status_code == 200

    data = response.json()

    assert len(data["documents"]) >= 1

    for document in data["documents"]:

        assert document["status"] == "queued"