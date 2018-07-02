
from src import db


class Article(db.Model):
    id = db.Column(db.Integer, primary_key=True)

    source_id = db.Column(db.String(50), nullable=False)
    url = db.Column(db.String(1024), nullable=False)

    text = db.Column(db.String(1024 * 32), nullable=True)

    language = db.Column(db.String(50), nullable=True)

    feed_id = db.Column(db.Integer, db.ForeignKey('feed.id'))
    feed = db.relationship("Feed", backref=db.backref('articles', lazy=True))
