from sqlalchemy.orm import relationship

from src import db


class Feed(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), nullable=True)
    url = db.Column(db.String(1024), unique=True, nullable=False)
