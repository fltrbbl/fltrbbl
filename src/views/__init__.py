from .user import User


import logging

from .. import api
from .user import UserView
from .feeds import FeedsView
from .feed import FeedView
from .trigger_update import TriggerUpdateView

logger = logging.getLogger(__name__)


api.add_resource(UserView, '/user')
api.add_resource(FeedView, '/feed')  # get your current feed
api.add_resource(FeedsView, '/feeds')  # manage feeds
api.add_resource(TriggerUpdateView, '/trigger_update')  # trigger db update

"""
@app.route('/feed', methods=['GET', 'POST'])
@login_required
def root():
    feed_url = request.args.get('feed_url', '')
    print(feed_url)

    feed = fetch_feed(feed_url)
    good, bad = decide(1, feed)
    good_feed = generate_feed_atom(good)

    return good_feed

@app.route('/docs', methods=['GET'])
def all_docs():
    d = {}
    for feed in Feed.objects:
        d['%s' % feed.url] = []
        for article in Article.objects(feed=feed):
            d['%s' % feed.url].append( {
                'text': article.text,
                'language': article.language,
                'url': article.url,
                'source_id': article.source_id
            })
    return jsonify(d)
"""



"""
{
  "api_key": "a2ef417edf582ffd28c4f8c4c41fcf4f", 
  "username": "testuser"
}

"""