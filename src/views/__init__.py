import logging

from .. import api
from .user import UserView
from .feeds import FeedsView
from .feed import FeedView
from .feed_xml import AtomView, RssView
from .trigger_update import TriggerUpdateView

logger = logging.getLogger(__name__)

api.add_resource(RssView, '/feed/rss')  # get your current feed
api.add_resource(AtomView, '/feed/atom')  # get your current feed

api.add_resource(UserView, '/user')
api.add_resource(FeedView, '/feed')  # get your current feed
api.add_resource(FeedsView, '/feeds')  # manage feeds
api.add_resource(TriggerUpdateView, '/trigger_update')  # trigger db update


