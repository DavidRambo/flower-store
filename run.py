from flower_store import create_app, db
from flower_store.models import Flower

app = create_app()


@app.shell_context_processor
def make_shell_context():
    """When the `flask shell` command runs, it invokes this function and
    registers the dictionary of items returned. Thus, the database instance
    'db' can be accessed in the shell session as 'db', and likewise for the
    SQLAlchemy model 'Flower'.
    """
    return {"db": db, "Flower": Flower}
