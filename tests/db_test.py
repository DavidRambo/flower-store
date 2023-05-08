def test_flower(client, app):
    """Tests the Flower model in the database."""
    response = client.post("/store")
    response.status_code = 200
