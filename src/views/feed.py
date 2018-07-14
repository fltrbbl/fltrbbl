import json
import datetime
import html
from feedgen.feed import FeedGenerator

from flask_restful import Resource

from flask_login import login_required, current_user

from src.models import Feed, User, Article
from flask import request, abort


class FeedView(Resource):
    method_decorators = {
        'get': [login_required],
        'post': [login_required]
    }

    def get(self):
        feeds = Feed.objects.filter(users__contains=current_user.id).all()
        articles = Article.objects.filter(feed__in=feeds).all()
        return articles.to_json()

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
            abort(404)  # feed not found

        User.objects(id=current_user.id).update_one(pull__feeds=feed)

        return User.objects(id=current_user.id).first().as_dict(), 201
