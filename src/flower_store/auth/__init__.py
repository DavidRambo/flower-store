from flask import Blueprint

bp = Blueprint("auth", __name__)

from flower_store.auth import routes
