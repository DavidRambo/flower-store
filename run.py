import dev_fns
from flower_store import create_app, db, cli
from flower_store.models import Flower, User

app = create_app()
cli.register(app)


@app.shell_context_processor
def make_shell_context():
    """When the `flask shell` command runs, it invokes this function and
    registers the dictionary of items returned. Thus, the database instance
    'db' can be accessed in the shell session as 'db', and likewise for the
    SQLAlchemy model 'Flower'.

    To run the dev functions in the shell, call them:
        - popf()
        - ca()
    """
    return {
        "db": db,
        "Flower": Flower,
        "User": User,
        "popf": dev_fns.populate_flowers,
        "ca": dev_fns.create_admin,
    }
