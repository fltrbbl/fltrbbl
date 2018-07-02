import logging
import os

from flask import Flask, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_admin import Admin
from flask_login import LoginManager


logging.basicConfig(level=logging.DEBUG)

app = Flask(__name__)
app.config['SECRET_KEY'] = 'skjdvnakjfdnakdsvzuewqoiufed'
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgres://postgres:%s@db' % os.environ['POSTGRES_PASSWORD']
db = SQLAlchemy(app)
migrate = Migrate(app, db)

login_manager = LoginManager()
login_manager.init_app(app)

@login_manager.request_loader
def load_user_from_request(request):
    api_key = request.args.get('api_key')
    if api_key:
        user = User.query.filter_by(api_key=api_key).first()
        if user:
            return user

    # finally, return None if both methods did not login the user
    return None

admin = Admin(app, name='news_spam_thing', template_mode='bootstrap3')

from .app import *
from .cli import *
from .models import *
from .admin import *



