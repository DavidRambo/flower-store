from flower_store import cli, create_app, db
from flower_store.models import Flower, User

app = create_app()
cli.register(app)


@app.shell_context_processor
def make_shell_context():
    """When the `flask shell` command runs, it invokes this function and
    registers the dictionary of items returned. Thus, the database instance
    'db' can be accessed in the shell session as 'db', and likewise for the
    SQLAlchemy model 'Flower'.
    """
    return {
        "db": db,
        "Flower": Flower,
        "User": User,
    }
