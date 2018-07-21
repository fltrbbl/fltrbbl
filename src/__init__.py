import logging

from flask import Flask, jsonify
from flask_login import LoginManager
from flask_mongoengine import MongoEngine
from flask_restful import Api
from flask_cors import CORS

logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

matplotlib_logger = logging.getLogger('matplotlib')
matplotlib_logger.setLevel(logging.WARNING)

app = Flask(__name__)
app.config['SECRET_KEY'] = 'skjdvnakjfdnakdsvzuewqoiufed'
app.config['MONGODB_SETTINGS'] = {
    'host': 'mongo',
    'db': 'fltrbbl',
    'port': 27017,

}

api = Api(app)
cors = CORS(app, resources={r"*": {"origins": "*"}})

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
    if auth and auth.username and auth.password:
        logger.debug('trying basic auth...')
        user = User.objects(email=auth.username).first()
        if user and user.verify_password(auth.password):
            logger.debug('found user %s!' % user.email)
            return user

    elif request.headers.get('Authorization', False):
        logger.debug('trying with token auth...')
        auth_header = request.headers['Authorization'].split('Token: ', 1)
        if len(auth_header) == 2:
            user = User.verify_auth_token(auth_header[1])
            logger.debug('found user %s!' % user.email)
            return user

    # finally, return None if both methods did not login the user
    return None
