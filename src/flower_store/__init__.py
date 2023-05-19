import os

from flask import Flask
from flask_admin import Admin
from flask_admin.contrib.sqla import ModelView
from flask_assets import Bundle, Environment
from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy

from flower_store.config import Config

# Create a database instance to represent the database.
db = SQLAlchemy()
# Do the same for the migration engine.
migrate = Migrate()

admin = Admin()


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

    # Setup admin app context and ModelViews
    admin.init_app(app)

    from flower_store.models import Flower

    admin.add_view(ModelView(Flower, db.session))

    # Instantiate Environment from Flask-Assets
    # Note that assets.init_app(app) is not sufficient to link to the app.
    assets = Environment(app)
    # assets.init_app(app)

    # All paths are relative to the app's static/ directory, or the static/
    # directory of a Flask blueprint
    css = Bundle("src/main.css", output="dist/main.css")
    js = Bundle("src/*.js", output="dist/main.js")
    assets.register("css", css)
    assets.register("js", js)
    css.build()
    js.build()

    from . import home
    from . import catalog
    from . import cart

    app.register_blueprint(home.bp)
    app.register_blueprint(catalog.bp)
    app.register_blueprint(cart.bp)

    app.add_url_rule("/", endpoint="home")

    return app
