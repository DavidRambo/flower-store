def test_store(client):
    """Tests the store page."""
    response = client.get("/store")
    response.status_code = 200
    assert b"Store - Flower Shop" in response.data
