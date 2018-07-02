from sqlalchemy.orm import relationship

from src import db


class Vote(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    like = db.Column(db.Boolean)

    article_id = db.Column(db.Integer, db.ForeignKey('article.id'))
    article = db.relationship("Article", backref=db.backref('likes', lazy=True))

    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    user = db.relationship("User", backref=db.backref('likes', lazy=True))
