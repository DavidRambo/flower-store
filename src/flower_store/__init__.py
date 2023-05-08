import os

from flask import Flask
from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy

from flower_store.config import Config

# Create a database instance to represent the database.
db = SQLAlchemy()
# Do the same for the migration engine.
migrate = Migrate()


def create_app(test_config=None):
    app = Flask(__name__, instance_relative_config=True)

    if test_config is None:
        app.config.from_object(Config)
        if not app.config["SQLALCHEMY_DATABASE_URI"]:
            app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///" + os.path.join(
                app.instance_path, "flowers.db"
            )
    else:
        app.config.from_mapping(test_config)

    # ensure the instance folder exists
    try:
        os.makedirs(app.instance_path)
    except OSError:
        pass

    db.init_app(app)
    migrate.init_app(app, db)

    from . import home
    from . import store
    from . import cart

    app.register_blueprint(home.bp)
    app.register_blueprint(store.bp)
    app.register_blueprint(cart.bp)

    app.add_url_rule("/", endpoint="home")

    return app
