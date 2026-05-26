from bson import ObjectId


async def test_submit_document_success(async_client):

    payload = {
        "user_id": "user1",
        "title": "Test Document",
        "content": "This is a valid test document content"
    }

    response = await async_client.post(
        "/documents",
        json=payload
    )

    assert response.status_code == 200

    data = response.json()

    assert "document_id" in data
    assert data["status"] == "queued"


async def test_submit_document_invalid_payload(async_client):

    payload = {
        "user_id": "",
        "title": "",
        "content": "abc"
    }

    response = await async_client.post(
        "/documents",
        json=payload
    )

    assert response.status_code == 422


async def test_get_document_status(async_client):

    payload = {
        "user_id": "user1",
        "title": "Test",
        "content": "This is document content"
    }

    create_response = await async_client.post(
        "/documents",
        json=payload
    )

    document_id = create_response.json()["document_id"]

    response = await async_client.get(
        f"/documents/{document_id}"
    )

    assert response.status_code == 200

    data = response.json()

    assert data["document_id"] == document_id
    assert data["status"] == "queued"


async def test_get_invalid_document(async_client):

    fake_id = str(ObjectId())

    response = await async_client.get(
        f"/documents/{fake_id}"
    )

    assert response.status_code == 404


async def test_invalid_object_id(async_client):

    response = await async_client.get(
        "/documents/abc123"
    )

    assert response.status_code == 400