
from src import db

class Feed(db.Document):
    title = db.StringField()
    url = db.StringField(required=True)

    articles = db.ListField(db.ReferenceField("Article"))

    users = db.ListField(db.ReferenceField("User"))

    def as_dict(self):
        return dict(
            title=self.title,
            url=self.url
        )

    def __repr__(self):
        return '<Feed %r (%s)>' % (self.title, self.url)
