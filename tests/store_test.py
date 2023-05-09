def test_catalog(client):
    """Tests the catalog page."""
    response = client.get("/catalog")
    response.status_code = 200
    assert b"Catalog - Flower Shop" in response.data
