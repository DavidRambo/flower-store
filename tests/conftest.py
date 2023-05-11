# import os
# import tempfile

import pytest

from flower_store import create_app, db
from flower_store.models import Flower


@pytest.fixture()
def app():
    """Main setup fixture."""
    # db_fd, db_path = tempfile.mkstemp()

    app = create_app(
        {
            "TESTING": True,
            # "SQLALCHEMY_DATABASE_URI": "sqlite:///" + db_path + "test.db"
            "SQLALCHEMY_DATABASE_URI": "sqlite://",
            "PER_PAGE": 12,
        }
    )

    with app.app_context():
        db.create_all()

    yield app

    # os.close(db_fd)
    # os.unlink(db_path)


@pytest.fixture()
def client(app):
    """Tests will use the client to make requests to the application without
    running the server.
    """
    return app.test_client()


@pytest.fixture()
def setup_db(app):
    # Create three flowers
    f1 = Flower(name="Diva", stock=5)
    f2 = Flower(name="Daddy's Girl", stock=8)
    f3 = Flower(name="KA's Mocha Maya")

    with app.app_context():
        # Add to database
        db.session.add(f1)
        db.session.add(f2)
        db.session.add(f3)
        db.session.commit()
