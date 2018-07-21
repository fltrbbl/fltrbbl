import secrets

from passlib.apps import custom_app_context as pwd_context
from src import db, app

from .feed import Feed

from itsdangerous import TimedJSONWebSignatureSerializer as Serializer, BadSignature, SignatureExpired

class User(db.Document):
    email = db.StringField(required=True)
    password_hash = db.StringField()
    api_key = db.StringField(default=secrets.token_hex(16))


    def as_dict(self):
        feeds = Feed.objects.filter(users__contains=self)

        return dict(
            email=self.email,
            api_key=self.api_key,
            feeds=[{'url': feed.url, 'title': feed.title} for feed in feeds]
        )

    def hash_password(self, password):
        self.password_hash = pwd_context.encrypt(password)

    def verify_password(self, password):
        return pwd_context.verify(password, self.password_hash)

    def generate_auth_token(self, expiration=600):
        s = Serializer(app.config['SECRET_KEY'], expires_in=expiration)
        return s.dumps({'id': str(self.id)})

    @staticmethod
    def verify_auth_token(token):
        s = Serializer(app.config['SECRET_KEY'])
        try:
            data = s.loads(token)
        except SignatureExpired:
            return None  # valid token, but expired
        except BadSignature:
            return None  # invalid token
        user = User.objects.get(id=data['id'])
        return user

    @property
    def is_authenticated(self):
        return True

    @property
    def is_active(self):
        return True

    @property
    def is_anonymous(self):
        return False
