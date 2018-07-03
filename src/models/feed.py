from sqlalchemy.orm import relationship

from src import db


class Feed(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=True)
    url = db.Column(db.String(1024), unique=True, nullable=False)

    def __repr__(self):
        return '<Feed %r (%s)>' % (self.title, self.url)

