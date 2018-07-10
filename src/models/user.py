import secrets

from passlib.apps import custom_app_context as pwd_context
from src import db


class User(db.Document):
    email = db.StringField(required=True)
    password_hash = db.StringField()
    api_key = db.StringField(default=secrets.token_hex(16))

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
