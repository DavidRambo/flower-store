from flask_login import UserMixin
from werkzeug.security import check_password_hash, generate_password_hash

from flower_store import db, login


class Flower(db.Model):
    """Represents a row in the Users table, which SQLAlchemy will translate.

    db.Model is the base class for all models from Flask-SQLAlchemy. Fields
    are represented by the class's instance attributes, which are themselves
    created as instances of the db.Column class.
    """

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64), index=True, unique=True)
    stock = db.Column(db.Integer, default=0)
    image_file = db.Column(db.String(30), default="default.png")
    bloom_size = db.Column(db.Float(5))  # in inches
    height = db.Column(db.Float(5))  # in feet
    # form = db.Column(db.String(40))
    # color = db.Column(db.String(20))

    def __repr__(self):
        return f"<Flower: {self.name}, {self.stock}>"


class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(20), index=True, unique=True)
    email = db.Column(db.String(120), index=True, unique=True)
    password_hash = db.Column(db.String(128))
    is_admin = db.Column(db.Boolean, default=False)

    def __repr__(self):
        return f"<User {self.username}>"

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)


@login.user_loader
def load_user(id: str) -> User:
    """Queries the database's User table for the user with the provided id."""
    return User.query.get(int(id))
