import requests

from flask_restful import Resource

from flask_login import login_required, current_user

from src.models import Feed, User
from flask import request, abort


rss_and_atom_headers = [
    'application/rss+xml'
    'application/rss',
    'application/atom+xml'
    'application/atom'
]



class FeedsView(Resource):
    method_decorators = {
        'get': [login_required],
        'post': [login_required]
    }

    def get(self):
        return current_user.as_dict()['feeds'], 200

    def put(self):
        feed_url = request.json.get('url')

        if feed_url is None:
            abort(400)  # missing arguments

        feed = Feed.objects(url=feed_url).first()
        if feed is None:
            try:
                res = requests.get(feed_url)
            except requests.exceptions.ConnectionError as e:
                return 'error fetching this feed: %s' % (e), 400

            if not res.ok:
                return 'feed returned %s: %s' % (res.status_code, res.content), 400

            if not res.headers.get('Content-Type', False) not in rss_and_atom_headers:
                return 'feed is not rss or atom: %s' % res.headers.get('Content-Type', False), 400

            feed = Feed(url=feed_url)
            feed.save()

        if current_user not in feed.users:
            feed.users.append(current_user.id)
            feed.save()

        return current_user.as_dict()['feeds'], 201

    def delete(self):
        feed_url = request.json.get('url', False) if request.json else False
        if not feed_url:
            feed_url = request.args.get('url', False)

        if not feed_url:
            abort(400)  # missing arguments

        feed = Feed.objects(url=feed_url).first()
        if feed is None:
            abort(404) # feed not found

        Feed.objects(url=feed_url).update_one(pull__users=current_user.id)

        return current_user.as_dict()['feeds'], 201

