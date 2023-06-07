from flask_login import UserMixin
from werkzeug.security import check_password_hash, generate_password_hash

from flower_store import db, login
from flower_store.search import add_to_index, remove_from_index, query_index


class SearchableMixin(object):
    """A mixin class to provide interface between SQLAlchemy and Elasticsearch.

    Modeled on Migeul Grinberg's Flask Mega-Tutorial, part 16.
    """

    @classmethod
    def search(cls, expression):
        """Wraps the flower_storesearch.query_index method, replacing the list of object
        IDs with actual objects. For example, when the mixin class is inherited
        by the Post model, cls.__tablename__ refers to the name that
        Flask-SQLAlchemy assigned to the relational table. It returns the list
        of result IDs and the total number of results.
        """
        ids, total = query_index(cls.__tablename__, expression)
        if total == 0:
            return cls.query.filter_by(id=0), 0
        when = []
        for idx, id in enumerate(ids):
            when.append((id, idx))
        return (
            cls.query.filter(cls.id.in_(ids)).order_by(db.case(*when, value=cls.id)),
            total,
        )

    @classmethod
    def before_commit(cls, session) -> None:
        session._changes = {
            "add": list(session.new),
            "update": list(session.dirty),
            "delete": list(session.deleted),
        }

    @classmethod
    def after_commit(cls, session) -> None:
        for obj in session._changes["add"]:
            if isinstance(obj, SearchableMixin):
                add_to_index(obj.__tablename__, obj)
        for obj in session._changes["update"]:
            if isinstance(obj, SearchableMixin):
                add_to_index(obj.__tablename__, obj)
        for obj in session._changes["delete"]:
            if isinstance(obj, SearchableMixin):
                add_to_index(obj.__tablename__, obj)

    @classmethod
    def reindex(cls) -> None:
        for obj in cls.query:
            add_to_index(cls.__tablename__, obj)


db.event.listen(db.session, "before_commit", SearchableMixin.before_commit)
db.event.listen(db.session, "after_commit", SearchableMixin.after_commit)


class Flower(SearchableMixin, db.Model):
    """Represents a row in the Users table, which SQLAlchemy will translate.

    db.Model is the base class for all models from Flask-SQLAlchemy. Fields
    are represented by the class's instance attributes, which are themselves
    created as instances of the db.Column class.

    : attr :
        __searchable__ : list of fields indexed by the search engine
    """

    __searchable__ = ["name"]

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64), index=True, unique=True)
    stock = db.Column(db.Integer, default=0)
    image_file = db.Column(db.String(30), default="default.png")
    bloom_size = db.Column(db.Float(5))  # in inches
    height = db.Column(db.Float(5))  # in feet
    price = db.Column(db.Float(5))  # in dollars US
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
