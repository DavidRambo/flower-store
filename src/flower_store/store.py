from flask import Blueprint, render_template

bp = Blueprint("store", __name__)


@bp.route("/store", methods=["GET"])
def store():
    """The store page shows all flowers in the database regardless of
    inventory.

    TODO: Search database for flowers.
    """
    return render_template("store.html", title="Store")


@bp.route("/store/<flower>", methods=["GET"])
def flower_page():
    """Individual flower's page."""
    pass
