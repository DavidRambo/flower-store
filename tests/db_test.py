from flower_store import db
from flower_store.models import Flower
from flower_store import catalog


def test_flowers_stock(app, setup_db):
    """Tests the Flower model in the database."""

    with app.app_context():
        # Confirm there are three entries in database
        assert Flower.query.count() == 3

        # Query the database for out-of-stock items
        oos = []
        for flower in Flower.query.filter_by(stock=0):
            oos.append(flower.name)

        assert "KA's Mocha Maya" in oos

        in_stock = {}
        for flower in Flower.query.all():
            if flower.stock:
                in_stock.update({flower.name: flower.stock})

        assert len(in_stock) == 2


def test_search(client, app, setup_db):
    """Tests the search route.

    The search route '/catalog/search' is activated via a POST request.
    """

    with app.app_context():
        # TODO: build template for view function that has a text form named "search"
        response = client.post("/catalog/search", data={"search": "ka"})
        assert response.status_code == 200  # I think this is correct.
        assert b"KA's Mocha Maya" in response.data
