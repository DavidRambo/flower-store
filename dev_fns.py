from random import randint
from random import shuffle

from flower_store import db
from flower_store.models import Flower


def dev_populate():
    """Populates the database with Flowers for the sake of development."""

    flowers = [
        "A-Peeling",
        "Bliss",
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
        "Tootles",
    ]
    shuffle(flowers)

    # Clear Flower table
    Flower.query.delete()

    for flower in flowers:
        db.session.add(Flower(name=flower, stock=randint(0, 10)))
        db.session.commit()
