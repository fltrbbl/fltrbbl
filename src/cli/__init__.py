
from .. import app
from src.models import User, Article, Feed, Vote

from src.ml.update_db import update_db


@app.cli.command()
def fetch_feeds():
    update_db()


@app.cli.command()
def flush_db():
    """flush the database."""
    User.objects.all().delete()
    Article.objects.all().delete()
    Feed.objects.all().delete()
    Vote.objects.all().delete()
