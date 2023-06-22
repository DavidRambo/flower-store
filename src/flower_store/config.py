import os
from dotenv import load_dotenv


basedir = os.path.abspath(os.path.dirname(__file__))
load_dotenv(os.path.join(basedir, ".env"))


class Config:
    """Configuration object for the Flask app. Checks the local .env file for
    values and sets default values otherwise.

    Attributes:
        SECRET_KEY : hex token used to secure encrypted backend requests.
        DATABASE_URL : location of the SQL database. Defaults to None, which
          tells the application factory to set an instance_path to the db.
    """

    SECRET_KEY = os.environ.get("SECRET_KEY") or "secret-key"
    # DATABASE_URI = os.environ.get("DATABASE_URI") or "sqlite:///" + os.path.join(
    #     basedir, "app.db"
    # )
    SQLALCHEMY_DATABASE_URI = os.environ.get("DATABASE_URL", None)

    SQLALCHEMY_TRACK_MODIFICATIONS = False

    # Number of flowers to show per page in the catalog.
    PER_PAGE = 12
