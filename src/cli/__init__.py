
from .. import app
from src.models import User, Article, Feed, Vote

@app.cli.command()
def fetch_feeds():
    pass


@app.cli.command()
def flush_db():
    """flush the database."""
    User.objects.all().delete()
    Article.objects.all().delete()
    Feed.objects.all().delete()
    Vote.objects.all().delete()
