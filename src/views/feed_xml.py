import json
import datetime
import html
from feedgen.feed import FeedGenerator

from flask_restful import Resource

from flask_login import login_required, current_user

from src.models import Feed, Article
from flask import make_response


def _format_to_xml(json_feed, format='atom'):
    fg = FeedGenerator()
    fg.id('fltrbbl')
    fg.title('fltrbbl')

    for item in json_feed:
        item: Article
        fe = fg.add_entry()

        fe.id(item.source_id)
        fe.title(item.title)
        for author in item.authors:
            fe.author(name=author)
        # fg.link(href=item.url, rel='alternate') # link to main page
        fe.link(href=item.url, rel='self')
        fe.guid(guid=item.source_id, permalink=item.url)
        if item.publish_date != None:
            fe.published(item.publish_date.replace(tzinfo=datetime.timezone.utc))
        fe.description(item.summary)

        fe.content(item.html, type='CDATA')

    if format == 'atom':
        return fg.atom_str(pretty=True)  # Get the ATOM feed as string
    elif format == 'rss':
        fg.rss_str(pretty=True)  # Get the RSS feed as string
    else:
        raise Exception('unknown format')


def make_rss_response(feed, code, headers=None):
    data = _format_to_xml(feed, 'rss')

    resp = make_response(data, code)
    resp.headers.extend(headers or {})
    return resp


class RssView(Resource):
    representations = {
        'application/xml': make_rss_response,
        'text/html': make_rss_response,
        'application/xhtml+xml': make_rss_response,
        'application/xml;q=0.9': make_rss_response,
    }
    method_decorators = {
        'get': [login_required],
    }

    def get(self):
        feeds = Feed.objects.filter(users__contains=current_user.id).all()
        articles = Article.objects.filter(feed__in=feeds).all()
        return articles


def make_atom_response(feed, code, headers=None):
    data = _format_to_xml(feed, 'atom')

    resp = make_response(data, code)
    resp.headers.extend(headers or {})
    return resp


class AtomView(Resource):
    representations = {
        'application/atom': make_atom_response,
        'application/atom+xml; charset=utf-8': make_atom_response,
    }
    method_decorators = {
        'get': [login_required],
    }

    def get(self):
        feeds = Feed.objects.filter(users__contains=current_user.id).all()
        articles = Article.objects.filter(feed__in=feeds).all()
        return articles
