async def test_rate_limit(async_client):

    payload = {
        "user_id": "rate_limit_user",
        "title": "Test",
        "content": "This is a long enough content"
    }

    responses = []

    for _ in range(4):

        response = await async_client.post(
            "/documents",
            json=payload
        )

        responses.append(response)

    assert responses[0].status_code == 200
    assert responses[1].status_code == 200
    assert responses[2].status_code == 200

    assert responses[3].status_code == 429

    assert (
        responses[3].json()["detail"]
        == "Too many active jobs"
    )