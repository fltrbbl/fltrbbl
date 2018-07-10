import secrets
import mongoengine

from passlib.apps import custom_app_context as pwd_context
from src import db

from .feed import Feed

class User(db.Document):
    email = db.StringField(required=True)
    password_hash = db.StringField()
    api_key = db.StringField(default=secrets.token_hex(16))

    feeds = db.ListField(db.ReferenceField(Feed, reverse_delete_rule=mongoengine.PULL))


    def as_dict(self):
        return dict(
            email=self.email,
            api_key=self.api_key,
            feeds=[{'url': feed.url, 'title': feed.title} for feed in self.feeds]
        )

    def hash_password(self, password):
        self.password_hash = pwd_context.encrypt(password)

    def verify_password(self, password):
        return pwd_context.verify(password, self.password_hash)

    @property
    def is_authenticated(self):
        return True

    @property
    def is_active(self):
        return True

    @property
    def is_anonymous(self):
        return False
