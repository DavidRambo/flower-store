import os

from flask import Flask
from flask_admin import Admin
from flask_assets import Bundle, Environment
from flask_login import LoginManager
from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy

from flower_store.config import Config

# Create a database instance to represent the database.
db = SQLAlchemy()
# Do the same for the migration engine.
migrate = Migrate()

admin = Admin()

login = LoginManager()


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
    from flower_store.models import Flower
    from flower_store.admin_views import MyAdminIndexView, FlowerView

    admin.init_app(app, index_view=MyAdminIndexView())
    admin.add_view(FlowerView(Flower, db.session))

    from sqlalchemy.event import listens_for
    from flower_store.admin_views import IMAGE_PATH

    @listens_for(Flower, "after_delete")
    def del_image(mapper, connection, target):
        if target.image_file:
            # Delete image
            try:
                os.remove(os.path.join(IMAGE_PATH, target.image_file))
            except OSError:
                pass

            # Delete thumbnail
            # try:
            #     os.remove(os.path.join(IMAGE_PATH, thumbgen_filename(target.path)))
            # except OSError:
            #     pass

    login.init_app(app)

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
    from . import auth

    app.register_blueprint(home.bp)
    app.register_blueprint(catalog.bp)
    app.register_blueprint(cart.bp)
    app.register_blueprint(auth.bp)

    app.add_url_rule("/", endpoint="home")

    return app
