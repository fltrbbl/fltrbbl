from flask_restful import Resource

from flask_login import login_required, current_user

from src.models import Feed, User
from flask import request, abort


class FeedView(Resource):
    method_decorators = {
        'get': [login_required],
        'post': [login_required]
    }

    def get(self):
        return [{'title': feed.title, 'url': feed.url} for feed in current_user.feeds], 200

    def put(self):
        feed_url = request.json.get('url')

        if feed_url is None:
            abort(400)  # missing arguments

        feed = Feed.objects(url=feed_url).first()
        if feed is None:
            feed = Feed(url=feed_url)
            feed.save()

        if feed not in current_user.feeds:
            current_user.feeds.append(feed)
            current_user.save()

        return current_user.as_dict(), 201

    def delete(self):
        feed_url = request.json.get('url')

        if feed_url is None:
            abort(400)  # missing arguments

        feed = Feed.objects(url=feed_url).first()
        if feed is None:
            abort(404) # feed not found

        User.objects(id=current_user.id).update_one(pull__feeds=feed)

        return User.objects(id=current_user.id).first().as_dict(), 201

