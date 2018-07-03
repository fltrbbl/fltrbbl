import click

from src import app
from src import db
from src.models import Article

@app.cli.command()
def fetch_feeds():
    pass


@app.cli.command()
def flush_feeds():
    """Initialize the database."""
    db.session.query(Article).delete()
    db.session.commit()