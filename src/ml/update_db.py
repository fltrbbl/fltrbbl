import feedparser
import logging
from time import sleep
from ..models import Article, Feed
from .. import db
from newspaper import Article as NewspaperArticle

from multiprocessing.pool import ThreadPool

logger = logging.getLogger(__name__)


def update_db():
    logger.info('updating db...')
    feeds = Feed.objects.all()
    logger.info('updating %s feeds' % len(feeds))
    pool = ThreadPool(5)

    pool.apply(update_feed, [feed.url for feed in feeds])
    logger.info('queued!')


def update_feed(feed_url):
    logger.info('processing feed %s' % feed_url)
    parsed_feed = feedparser.parse(feed_url)
    logger.debug('got parsed feed: %s articles' % len(parsed_feed))
    feed = Feed.objects.filter(url=feed_url).first()
    logger.debug('found %s' % feed)

    if feed.title is None:
        try:
            title = parsed_feed['feed']['title']
            logger.info('set title to %s' % title)
            feed.title = title
            feed.save()

        except Exception as e:
            logger.error(e)

    logger.debug('after title check')

    stored_article_source_ids = Article.objects.filter(feed=feed).all().values_list('source_id')
    print(stored_article_source_ids)

    logger.debug('checking %s articles...' % len(parsed_feed.entries))
    print(parsed_feed)
    for entry in parsed_feed.entries:
        print(entry)
        if entry.id not in stored_article_source_ids:
            logger.debug('fetching article...')
            newspaper_article = NewspaperArticle(entry.link)
            newspaper_article.download()
            newspaper_article.parse()

            article = Article(source_id=entry.id,
                              url=entry.link,
                              feed=feed,
                              text=newspaper_article.text,
                              language=newspaper_article.meta_lang
                              )
            article.save()
    logger.info('done with %s' % feed_url)
