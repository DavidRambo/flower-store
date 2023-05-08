from flower_store import db


class Flower(db.Model):
    """Represents a row in the Users table, which SQLAlchemy will translate.

    db.Model is the base class for all models from Flask-SQLAlchemy. Fields
    are represented by the class's instance attributes, which are themselves
    created as instances of the db.Column class.
    """

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64), index=True, unique=True)
    stock = db.Column(db.Integer, default=0)
    image_file = db.Column(db.String(20))

    def __repr__(self):
        return f"<Flower: {self.name}, {self.stock}>"
