import os
from dotenv import load_dotenv


basedir = os.path.abspath(os.path.dirname(__file__))
load_dotenv(os.path.join(basedir, ".env"))


class Config:
    """Configuration object for the Flask app. Checks the local .env file for
    values and sets default values otherwise.

    Attributes:
    """

    # hex token used to secure encrypted backend requests.
    SECRET_KEY = os.environ.get("SECRET_KEY") or "secret-key"

    # location of the SQL database. Defaults to None, which
    # tells the application factory to set an instance_path to the db.
    SQLALCHEMY_DATABASE_URI = os.environ.get("DATABASE_URL", None)

    SQLALCHEMY_TRACK_MODIFICATIONS = False

    # Number of flowers to show per page in the catalog.
    PER_PAGE = 12

    ELASTICSEARCH = os.environ.get("ELASTICSEARCH")
    ELASTICSEARCH_URL = os.environ.get("ELASTICSEARCH_URL")
    ELASTIC_KEY = os.environ.get("ELASTIC_KEY")
    ELASTIC_CERT = os.environ.get("ELASTIC_CERT")
