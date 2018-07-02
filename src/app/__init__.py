import logging

from flask import jsonify, request, abort
from flask_login import login_required
import urllib.parse

from src import app
from src import db
from src.models import User

from src.feedhandling.fetch import fetch_feed
from src.feedhandling.decide import decide
from src.feedhandling.generate import generate_feed_atom

from src.ml.update_db import update_db

logger = logging.getLogger(__name__)


@app.route('/api/users', methods=['POST'])
def new_user():
    username = request.json.get('username')
    password = request.json.get('password')

    if username is None or password is None:
        abort(400)  # missing arguments
    if User.query.filter_by(username=username).first() is not None:
        abort(400)  # existing user

    user = User(username=username)
    user.hash_password(password)

    db.session.add(user)
    db.session.commit()
    return jsonify({'username': user.username, 'api_key': user.api_key}), 201


@app.route('/feed', methods=['GET', 'POST'])
@login_required
def root():
    feed_url = request.args.get('feed_url', '')
    print(feed_url)

    feed = fetch_feed(feed_url)
    good, bad = decide(1, feed)
    good_feed = generate_feed_atom(good)

    return good_feed


@app.route('/poke')
@login_required
def poke():
    """
    trigger something

    :return:
    """
    logger.info('somebody poked...')

    update_db()

    return jsonify('triggered update'), 200



"""
{
  "api_key": "a2ef417edf582ffd28c4f8c4c41fcf4f", 
  "username": "testuser"
}

"""