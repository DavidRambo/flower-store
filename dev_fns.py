from random import randint, shuffle

from flower_store import db
from flower_store.models import Flower, User
from werkzeug.security import generate_password_hash


def populate_flowers():
    """Populates the database with Flowers for the sake of development."""

    flowers = [
        "A-Peeling",
        "Bride To Be",
        "Café au Lait",
        "Cheers",
        "Daddy's Girl",
        "Diva",
        "Fluffles",
        "Foxy Lady",
        "Ice Tea",
        "KA's Bella Luna",
        "KA's Blood Orange",
        "KA's Boho Peach",
        "KA's Cloud",
        "KA's Mocha Jake",
        "KA's Mocha Maya",
        "L'Ancress",
        "Lovebug",
        "Mai Tai",
        "Maki",
        "Marshmallow",
        "Maui",
        "Moonstruck",
        "Ranunculus",
        "Snapdragon",
        "Straw flower",
        "Tootles",
    ]
    shuffle(flowers)

    # Make sure `flower` table exists
    if not db.inspect(db.engine).has_table("flower"):
        print("Flower table does not exist. Run `flask db upgrade`")
        return

    # Clear Flower table
    Flower.query.delete()

    for flower in flowers:
        if flower == "Straw flower":
            db.session.add(
                Flower(
                    name=flower,
                    stock=randint(0, 10),
                    image_file="strawflower_edb8f2b8dc93.png",
                )
            )
        elif flower == "Ranunculus":
            db.session.add(
                Flower(
                    name=flower,
                    stock=randint(0, 10),
                    image_file="ranunculus_fc5fbcc0f.jpg",
                )
            )
        else:
            db.session.add(Flower(name=flower, stock=randint(0, 10)))

    db.session.commit()


def create_admin():
    """Creates an admin user account."""

    # Ensure `user` table exists
    if not db.inspect(db.engine).has_table("user"):
        print("User table does not exist. Run `flask db upgrade`")
        return

    test_admin = User(
        username="admin",
        email="test@test.com",
        is_admin=True,
    )
    # Check for existing "admin" user and delete if it exists.
    user = User.query.filter_by(username=test_admin.username).first()
    if user:
        db.session.delete(user)

    test_admin.set_password("test")
    db.session.add(test_admin)
    db.session.commit()
