import os
import tempfile

import pytest

from flower_store import create_app, db


@pytest.fixture
def app():
    """Main setup fixture."""
    db_fd, db_path = tempfile.mkstemp()

    app = create_app(
        {"TESTING": True, "SQLALCHEMY_DATABASE_URI": "sqlite:///" + db_path + "test.db"}
    )

    with app.app_context():
        db.create_all()

    yield app

    os.close(db_fd)
    os.unlink(db_path)


@pytest.fixture
def client(app):
    """Tests will use the client to make requests to the application without
    running the server.
    """
    return app.test_client()
