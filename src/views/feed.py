from flask_restful import Resource

from flask_login import login_required, current_user

from src.models import Feed, User, Article
from flask import request, abort
from webargs import fields
from webargs.flaskparser import use_kwargs


class FeedView(Resource):
    method_decorators = {
        'get': [login_required],
        'post': [login_required]
    }
    # https://stackoverflow.com/a/38480524

    get_args = {
        'page': fields.Int(
            required=False,
            missing=1,
        ),
        'pagesize': fields.Int(
            required=False,
            missing=10,
        )
    }

    @use_kwargs(get_args)
    def get(self, page, pagesize):
        feeds = Feed.objects.filter(users__contains=current_user.id).all()
        # paginate returns .items

        query = Article.objects.filter(feed__in=feeds).order_by('-publish_date')

        articles = query.paginate(page=page, per_page=pagesize)

        return [article.as_dict() for article in articles.items]

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
