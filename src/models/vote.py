from sqlalchemy.orm import relationship

from src import db

from .user import User
from .article import Article

class Vote(db.Document):
    like = db.BooleanField()

    article = db.ReferenceField(Article)
    user = db.ReferenceField(User)
