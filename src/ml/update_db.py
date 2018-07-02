import feedparser
import logging

from ..models import Article as ArticleModel, Feed as FeedModel
from .. import db
from newspaper import Article

from multiprocessing.pool import ThreadPool

logger = logging.getLogger(__name__)

def update_db():
    logger.info('updating db...')
    feeds = FeedModel.query.all()
    logger.info('updating %s feeds' % len(feeds))
    pool = ThreadPool(5)

    pool.apply_async(update_feed, [feed.url for feed in feeds])
    logger.info('queued!')


def update_feed(feed_url, feed_xml=None):
    if not feed_xml:
        parsed_feed = feedparser.parse(feed_url)
    else:
        parsed_feed = feedparser.parse(feed_xml)

    feed = FeedModel.query.filter_by(url=feed_url).first()
    if not feed:
        feed = FeedModel(url=feed_url)

    if not feed.title:
        feed.title = parsed_feed['feed']['title']

        db.session.add(feed)
        db.session.commit()


    stored_articles = feed.articles
    stored_article_source_ids = [article.source_id for article in stored_articles]
    for entry in parsed_feed.entries:
        if entry.id not in stored_article_source_ids:
            newspaper_article = Article(entry.link)
            newspaper_article.download()
            newspaper_article.parse()

            article = ArticleModel(source_id=entry.id,
                                   url=entry.link,
                                   feed=feed,
                                   text=newspaper_article.text,
                                   language=newspaper_article.meta_lang
                                   )
            db.session.add(article)
    db.session.commit()
