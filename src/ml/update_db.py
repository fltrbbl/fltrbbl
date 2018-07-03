import feedparser
import logging
from time import sleep
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


def update_feed(feed_url):

    logger.info('processing feed %s' % feed_url)
    parsed_feed = feedparser.parse(feed_url)
    logger.debug('got parsed feed...')
    feed = FeedModel.query.filter_by(url=feed_url).first()
    logger.debug('found %s' % feed)

    if not feed:
        logger.info('creating feed in db')
        feed = FeedModel(url=feed_url)
        db.session.add(feed)
        db.session.commit()
    logger.debug('after feed check')

    if feed.title is None:
        try:
            title = parsed_feed['feed']['title']
            logger.info('set title to %s' % title)
            feed.title = title

            db.session.add(feed)
            db.session.commit()
        except Exception as e:
            logger.error(e)

    logger.debug('after title check')

    stored_articles = feed.articles
    stored_article_source_ids = [article.source_id for article in stored_articles]
    logger.debug('checking %s articles...' % len(parsed_feed.entries))

    for entry in parsed_feed.entries:
        if entry.id not in stored_article_source_ids:
            logger.debug('fetching article...')
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
    logger.info('done with %s' % feed_url)
