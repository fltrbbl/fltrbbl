import requests
import logging

from xml.etree import ElementTree as etree
from copy import deepcopy

from .. import db
from ..models import Feed as FeedModel

logger = logging.getLogger(__name__)


class Feed:
    def __init__(self, url):
        self.url = url
        self.xml = None
        self._empty_feed = None

        self.generated_feed = None

        self.fetch()
        self.set_empty_feed()

    def ensure_feed_in_db(self):
        f = FeedModel.query(url=self.url).first()
        if not f:
            f = FeedModel(url=self.url)
            db.session.add(f)
            db.commit()


    def fetch(self):
        res = requests.get(self.url)
        logger.debug(res.text)
        self.xml = res.text

    def set_empty_feed(self):
        root = etree.fromstring(self.xml)
        items = root.findall('channel/item')
        for item in items:
            try:
                item.getparent().remove(item)
            except AttributeError as e:
                logger.error(e)
        self._empty_feed = deepcopy(root)
        self.generated_feed = deepcopy(root)

    def items(self):
        root = etree.fromstring(self.xml)
        items = root.findall('channel/item')
        return items

    def add_item(self, item):
        self.generated_feed.find('channel').append(item)

    def to_string(self):
        return etree.tostring(self.generated_feed)


def fetch_feed(feed_url):
    logger.info('processing feed %s' % feed_url)
    feed = Feed(feed_url)
    return feed
