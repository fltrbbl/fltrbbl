
from src import db
from .feed import Feed

class Article(db.Document):
    feed = db.ReferenceField(Feed, required=True)
    source_id = db.StringField(required=True)

    url = db.StringField()

    text = db.StringField()

    language = db.StringField()
