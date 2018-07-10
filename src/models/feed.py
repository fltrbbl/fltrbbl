from sqlalchemy.orm import relationship

from src import db


class Feed(db.Document):
    title = db.StringField()
    url = db.StringField(required=True)

    def __repr__(self):
        return '<Feed %r (%s)>' % (self.title, self.url)
