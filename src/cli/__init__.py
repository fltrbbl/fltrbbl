import click

from src import app
from src import db


@app.cli.command()
def initdb():
    """Initialize the database."""
    db.create_all()


@app.cli.command()
def fetch_feeds():
    pass
