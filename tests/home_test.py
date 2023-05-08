def test_home(client):
    """Tests the home page."""
    response = client.get("/")
    assert response.status_code == 200
    assert b"<title>Flower Shop</title>" in response.data
