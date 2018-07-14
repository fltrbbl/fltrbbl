import logging

from .. import app
from src.models import User, Article, Feed, Vote

from src.ml.update_db import update_db

logger = logging.getLogger(__name__)

@app.cli.command()
def fetch_feeds():
    logger.info('starting updatedb')
    update_db()
    logger.info('starting updatedb')


@app.cli.command()
def flush_db():
    """flush the database."""
    User.objects.all().delete()
    Article.objects.all().delete()
    Feed.objects.all().delete()
    Vote.objects.all().delete()


@app.cli.command()
def flush_articles():
    Article.objects.all().delete()
