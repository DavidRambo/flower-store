"""Routes for browsing, searching, and viewing flowers in the database."""
from flask import Blueprint, current_app, render_template, request, url_for

from flower_store.models import Flower

bp = Blueprint("catalog", __name__)


@bp.route("/catalog", methods=["GET"])
def catalog():
    """The catalog page shows all flowers in the database regardless of
    inventory.
    """
    page = request.args.get("page", 1, type=int)
    flowers = Flower.query.order_by(Flower.name).paginate(
        page=page, per_page=current_app.config["PER_PAGE"], error_out=False
    )
    next_url = (
        url_for("catalog.catalog", page=flowers.next_num) if flowers.has_next else None
    )
    prev_url = (
        url_for("catalog.catalog", page=flowers.prev_num) if flowers.has_prev else None
    )
    return render_template(
        "catalog.html",
        title="Catalog",
        flowers=flowers.items,
        next_url=next_url,
        prev_url=prev_url,
    )


@bp.route("/catalog/<flower_id>", methods=["GET"])
def flower(flower_id):
    """Individual flower's page."""
    pass
    flower = Flower.query.filter_by(id=flower_id).first()

    image_file = url_for("static", filename="flower_imgs/" + flower.image_file)
    return render_template(
        "full_flower.html", title=flower.name, flower=flower, image_file=image_file
    )


@bp.route("/search", methods=["GET"])
def search():
    return render_template("search.html", title="Search")


@bp.route("/search_results", methods=["POST"])
def search_results():
    """Renders a template displaying search results from the Flower database."""
    # Retrieve search string from field with name="q"
    search_term: str = request.args.get("search")
    print(search_term)

    if search_term:
        print(">>> searching...")
        page = request.args.get("page", 1, type=int)
        query = Flower.query.filter(Flower.name.ilike("%" + search_term + "%"))
        flowers_sorted = query.order_by(Flower.name).paginate(
            page=page, per_page=current_app.config["PER_PAGE"], error_out=False
        )
        return render_template("results.html", flower_ids=flowers_sorted)
    return ""


def query_flowers(q: str) -> list[int]:
    """Returns a list of ID ints corresponding to Flower entries in the db,
    sorted alphabetically by name.
    """
    # Get matching Flower entries.
    query = Flower.query.filter(Flower.name.ilike("%" + q + "%"))

    # Extract name and id
    name_id = {flower.name: flower.id for flower in query}

    # Return list of IDs (primary keys in db) sorted by name of Flower.
    return [name_id[f] for f in sorted(name_id)]
