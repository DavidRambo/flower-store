from flask import Blueprint, render_template

bp = Blueprint("store", __name__)


@bp.route("/store", methods=["GET"])
def store():
    return render_template("store.html", title="Store")
