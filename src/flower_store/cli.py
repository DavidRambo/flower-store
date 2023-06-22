import os
from random import randint, shuffle

from dotenv import load_dotenv

from flower_store import db
from flower_store.models import Flower, User


def register(app):
    @app.cli.command("pop-flowers")
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
                        price=35.00,
                    )
                )
            elif flower == "Ranunculus":
                db.session.add(
                    Flower(
                        name=flower,
                        stock=randint(0, 10),
                        image_file="ranunculus_fc5fbcc0f.jpg",
                        price=35.00,
                    )
                )
            else:
                db.session.add(Flower(name=flower, stock=randint(0, 10), price=35.00))

        db.session.commit()

    @app.cli.command("setup-admin")
    def setup_admin():
        """Creates an admin user account."""

        # Ensure `user` table exists
        if not db.inspect(db.engine).has_table("user"):
            print("User table does not exist. Run `flask db upgrade`")
            return

        admin = os.environ.get("ADMIN")
        admin_pwd = os.environ.get("ADMIN_PWD")

        test_admin = User(
            username=admin,
            email="davidrambo@mailfence.com",
            is_admin=True,
        )
        # Check for existing "admin" user and delete if it exists.
        user = User.query.filter_by(username=test_admin.username).first()
        if user:
            db.session.delete(user)

        test_admin.set_password(admin_pwd)
        db.session.add(test_admin)
        db.session.commit()
