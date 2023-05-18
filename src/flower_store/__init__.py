import os

from flask import Flask
from flask_assets import Bundle, Environment
from flask_login import LoginManager
from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy

from flower_store.config import Config

# Create a database instance to represent the database.
db = SQLAlchemy()
# Do the same for the migration engine.
migrate = Migrate()
# Create and initialize Flask-Login
login = LoginManager()
# Next, provide the name of the view function or endpoint (the same argument
# that gets passed to url_for()) so that the LoginManager knows how to redirect
# users not logged in when trying to visit certain pages.
login.login_view = "admin.login"
login.login_message = "Please log in to access this page."


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
    login.init_app(app)

    # Instantiate Environment from Flask-Assets
    # Note that assets.init_app(app) is not sufficient to link to the app.
    assets = Environment(app)

    # All paths are relative to the app's static/ directory, or the static/
    # directory of a Flask blueprint
    css = Bundle("src/main.css", output="dist/main.css")
    js = Bundle("src/*.js", output="dist/main.js")
    assets.register("css", css)
    assets.register("js", js)
    css.build()
    js.build()

    # Import and register blueprints
    from . import home
    from . import catalog
    from . import cart
    from .errors import handlers
    from .admin.routes import admin_bp

    app.register_blueprint(home.bp)
    app.register_blueprint(catalog.bp)
    app.register_blueprint(cart.bp)
    app.register_blueprint(handlers.bp)
    app.register_blueprint(admin_bp)

    app.add_url_rule("/", endpoint="home")

    return app
