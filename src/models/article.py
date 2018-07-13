from src import db
from .feed import Feed


class Article(db.Document):
    feed = db.ReferenceField(Feed, required=True)
    source_id = db.StringField(required=True)
    url = db.StringField()

    title = db.StringField()
    top_image = db.StringField()
    movies = db.ListField()
    keywords = db.ListField()
    tags = db.ListField()
    authors = db.ListField()
    publish_date = db.DateTimeField()
    summary = db.StringField()

    meta_data = db.DictField()

    language = db.StringField()

    text = db.StringField()
