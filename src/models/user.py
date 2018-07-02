import secrets

from passlib.apps import custom_app_context as pwd_context
from flask_login import UserMixin
from src import db


class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)

    password_hash = db.Column(db.String(128))

    api_key = db.Column(db.String(128), default=secrets.token_hex(16))

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