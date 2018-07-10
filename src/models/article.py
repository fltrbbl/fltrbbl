
from src import db
from .feed import Feed

class Article(db.Document):

    feed_url = db.ReferenceField(Feed, required=True)
    source_id = db.StringField()
    url = db.StringField()

    text = db.StringField()

    language = db.StringField()
