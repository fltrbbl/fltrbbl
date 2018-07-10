import logging
import os
import base64

from flask import Flask, jsonify
from flask_login import LoginManager
from flask_mongoengine import MongoEngine
from flask_restful import Api

logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

app = Flask(__name__)
app.config['SECRET_KEY'] = 'skjdvnakjfdnakdsvzuewqoiufed'
app.config['MONGODB_SETTINGS'] = {
    'host': 'mongo',
    'db': 'fltrbbl',
    'port': 27017,

}

api = Api(app)

login_manager = LoginManager()
login_manager.init_app(app)

db = MongoEngine()
db.init_app(app)

from .models import Article, Feed, User, Vote
from .views import *

from .cli import *


@login_manager.request_loader
def load_user_from_request(request):
    api_key = request.args.get('api_key')
    if api_key:
        logger.debug('found api key...')
        user = User.objects(api_key=api_key).first()
        if user:
            return user

    # next, try to login using Basic Auth
    auth = request.authorization
    logger.debug('auth: %s' % auth)
    if auth and auth.username and auth.password:
        logger.debug('trying with basic auth...')
        user = User.objects(email=auth.username).first()
        if user.verify_password(auth.password):
            return user

    # finally, return None if both methods did not login the user
    return None
