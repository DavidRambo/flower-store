from flask import Blueprint, render_template

bp = Blueprint("cart", __name__)


@bp.route("/cart", methods=["GET"])
def cart():
    return render_template("cart.html", title="Shopping Cart")
