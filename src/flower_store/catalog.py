from flask import Blueprint, render_template, request, url_for

from flower_store.models import Flower

bp = Blueprint("store", __name__)


@bp.route("/catalog", methods=["GET"])
def catalog():
    """The catalog page shows all flowers in the database regardless of
    inventory.
    """
    return render_template("catalog.html", title="Catalog")


@bp.route("/catalog/<flower_id>", methods=["GET"])
def flower(flower_id):
    """Individual flower's page."""
    pass
    flower = Flower.query.filter_by(id=flower_id)

    image_file = url_for("static", filename="flower_imgs/" + flower.image_file)
    return render_template(
        "full_flower.html", title=flower.name, flower=flower, image_file=image_file
    )


@bp.route("/catalog/search", methods=["POST"])
def search():
    """Renders a template displaying search results from the Flower database."""
    # Retrieve search string from field with name="q"
    q: str = request.args.get("q")
    if q:
        flower_ids: list[int] = query_flowers(q)
        return render_template("results.html", flower_ids=flower_ids)
    return ""


def query_flowers(q: str) -> list[int]:
    """Returns a list of ID ints corresponding to Flower entries in the db,
    sorted alphabetically by name.
    """
    # Get matching Flower entries.
    flowers = Flower.query.filter(Flower.name.ilike("%" + q + "%"))

    # Extract name and id
    name_id = {f.name: f.id for f in flowers}

    return [name_id[f] for f in sorted(name_id)]
