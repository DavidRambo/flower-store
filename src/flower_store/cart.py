from collections import defaultdict

from flask import Blueprint, flash, redirect, render_template, request, session, url_for

from flower_store import db
from flower_store.models import Flower

bp = Blueprint("cart", __name__)


# NOTE: Don't forget to declare `session.modified = True` after modifying mutable data.
# "Be advised that modifications on mutable structures are not picked up automatically,
# in that situation you have to explicitly set the attribute to True yourself."
# - https://flask.palletsprojects.com/en/2.3.x/api/#flask.session.modified

# TODO: Maybe? Abstract the cart item to a class, maybe a dataclass, so that modifying
# it is both more legible and easier to manage.


@bp.route("/cart", methods=["GET"])
def cart():
    # First check that the cart has been instantiated.
    if "cart" not in session or not session["cart"]:
        return render_template("cart.html", title="Shopping Cart", cart=None)

    # Evaluate items in the cart to ensure still in stock.
    messages = _check_cart()
    if messages:
        for message in messages:
            flash(message)

    # Query database for flowers in cart, creating a list of tuples comprising the
    # id, name of the flower, the quantity in cart, and the total price.
    flowers_in_cart = []
    total: float = 0
    for id in session["cart"]:
        flower = Flower.query.filter(Flower.id == id).first()
        quantity = session["cart"][id]
        flowers_in_cart.append(
            (
                flower.id,
                flower.name,
                quantity,
                "${:.2f}".format(flower.price * quantity),
                flower.stock,
            )
        )
        total += flower.price * quantity

    return render_template(
        "cart.html",
        title="Shopping Cart",
        cart=flowers_in_cart,
        total="${:.2f}".format(total),
    )


@bp.route("/cart/add/<flower_id>", methods=["POST"])
def add(flower_id):
    """Adds one flower of `flower_id` to the shopping cart."""
    # Ensure that the flower is in stock.
    flower = Flower.query.filter(Flower.id == flower_id).first()
    if flower is None or flower.stock < 1:
        flash("That flower is out of stock.")
        return redirect(url_for("catalog.flower", flower_id=flower_id))

    # Check whether the shopping cart has already been declared in this session.
    if "cart" not in session:
        # Create the shopping cart in the session.
        session["cart"] = defaultdict(int)

    # Add the flower to it.
    quantity = int(request.form.get("quantity"))
    if flower_id not in session["cart"]:
        session["cart"][flower_id] = quantity
    else:
        session["cart"][flower_id] += quantity
        # If the above pushes the cart quantity over the amount in stock, then
        # it will be corrected when going to the cart.

    session.modified = True

    return redirect(url_for("cart.cart"))


@bp.route("/cart/update/<flower_id>", methods=["POST"])
def update(flower_id):
    """Updates the quantity in the shopping cart."""
    new_quantity = int(request.form.get("quantity"))

    if new_quantity == 0:
        # Remove from cart.
        return redirect(url_for("cart.remove", flower_id=flower_id))

    if session["cart"][flower_id] == new_quantity:
        # Quantity is the same.
        return redirect(url_for("cart.cart"))

    # Update to new quantity.
    session["cart"][flower_id] = new_quantity
    session.modified = True
    flash("Cart updated.")
    return redirect(url_for("cart.cart"))


@bp.route("/cart/remove/<flower_id>", methods=["POST"])
def remove(flower_id):
    """Removes flower with `flower_id` from cart."""
    try:
        del session["cart"][flower_id]
        session.modified = True
        flower_name = Flower.query.filter(Flower.id == flower_id).first().name
        flash(f"{flower_name} removed from cart.")
        return redirect(url_for("cart.cart"))
    except KeyError:
        flash("Invalid item number.")
        return redirect(url_for("cart.cart"))


@bp.route("/cart/checkout", methods=["GET"])
def checkout():
    """Moves to the checkout page.

    Currently no payment is implemented, so this is only for proof of concept.
    The user will have the option to submit their order or return to cart.
    """
    return render_template("checkout.html", title="Checkout")


@bp.route("/cart/submit", methods=["POST"])
def submit():
    """Submits the order, clears the cart in the session, and reduces stock."""
    # Go through cart, reducing stock of flowers.
    for id, quantity in session["cart"].items():
        flower = Flower.query.filter(Flower.id == id).first()
        flower.stock -= quantity

    db.session.commit()

    # Clear the shopping cart.
    session["cart"].clear()

    flash("Order submitted!")
    return redirect(url_for("cart.cart"))


def _check_cart() -> list[str] | None:
    """Goes through the session's shopping cart to check for items that are
    either out of stock or understocked relative to the amount currently in the
    cart. It any are found, it removes them and returns a list of strings to
    be flashed to the user.
    """
    messages = []
    for flower_id in session["cart"]:
        flower = Flower.query.filter(Flower.id == flower_id).first()
        if flower is None or flower.stock < 1:
            del session["cart"][flower_id]
            messages.append(f"{flower.name} is no longer in stock.")
        elif session["cart"][flower_id] > flower.stock:
            messages.append(f"{flower.name} stock has been reduced to {flower.stock}.")
            session["cart"][flower_id] = flower.stock

    # Not sure that this is necessary since a key in the dict is being deleted.
    session.modified = True
    return messages if len(messages) > 0 else None
