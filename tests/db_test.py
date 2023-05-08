from flower_store import db
from flower_store.models import Flower


def test_flower(client, app):
    """Tests the Flower model in the database."""
    # Create three flowers
    f1 = Flower(name="Diva", stock=5)
    f2 = Flower(name="Daddy's Girl", stock=8)
    f3 = Flower(name="KA's Mocha Maya")

    with app.app_context():
        # Add to database
        db.session.add(f1)
        db.session.add(f2)
        db.session.add(f3)

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
