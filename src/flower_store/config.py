import os
from dotenv import load_dotenv


basedir = os.path.abspath(os.path.dirname(__file__))
load_dotenv(os.path.join(basedir, ".env"))


class Config:
    """Configuration object for the Flask app. Checks the local .env file for
    values and sets default values otherwise.

    Attributes:
        SECRET_KEY : hex token used to secure encrypted backend requests.
        DATABASE_URI : location of the SQL database. Defaults to None and
          allows the application factory to set an instance_path to the db.
    """

    SECRET_KEY = os.environ.get("SECRET_KEY") or "secret-key"
    # DATABASE_URI = os.environ.get("DATABASE_URI") or "sqlite:///" + os.path.join(
    #     basedir, "app.db"
    # )
    SQLALCHEMY_DATABASE_URI = os.environ.get("SQLALCHEMY_DATABASE_URI") or None
    SQLALCHEMY_TRACK_MODIFICATIONS = False
