import feedparser
import logging
import datetime

from time import sleep
from ..models import Article, Feed
from .. import db
from newspaper import Article as NewspaperArticle
from newspaper.article import ArticleDownloadState
import newspaper

from multiprocessing.pool import ThreadPool

logger = logging.getLogger(__name__)


def update_db():
    logger.info('updating db...')
    feeds = Feed.objects.all()
    logger.info('updating %s feeds' % len(feeds))
    pool = ThreadPool(5)

    pool.map(update_feed, [feed.url for feed in feeds])
    logger.info('queued!')


def update_feed(feed_url):
    logger.info('processing feed %s' % feed_url)
    parsed_feed = feedparser.parse(feed_url)
    logger.debug('got parsed feed: %s articles' % len(parsed_feed))
    feed = Feed.objects.filter(url=feed_url).first()

    if feed.title is None:
        try:
            title = parsed_feed['feed']['title']
            logger.info('set title to %s' % title)
            feed.title = title
            feed.save()

        except Exception as e:
            logger.error(e)

    stored_article_source_ids = Article.objects.filter(feed=feed).only('source_id').all().values_list('source_id')

    entry_ids = [entry.id for entry in parsed_feed.entries]

    # set articles not served by the source to inactive
    Article.objects(active=True, source_id__nin=entry_ids, feed=feed).update(active=False)

    # set articles served by the source to active
    #Article.objects(source_id__in=entry_ids, feed=feed).update(active=True)

    logger.info('%s active, %s in active articles in %s' % (Article.objects(active=True).count(), Article.objects(active=False).count(), feed_url))

    logger.debug('checking %s articles...' % len(parsed_feed.entries))
    for entry in parsed_feed.entries:
        if entry.id not in stored_article_source_ids:
            logger.debug('fetching article...')
            newspaper_article = NewspaperArticle(entry.link, keep_article_html=True)
            newspaper_article.download()
            if not newspaper_article.download_state == ArticleDownloadState.SUCCESS:
                # download failed - just skip
                continue

            newspaper_article.parse()

            article = Article(source_id=entry.id,
                              url=entry.link,
                              feed=feed,
                              active=True
                              )

            article.title = newspaper_article.title
            article.top_image = newspaper_article.top_image

            article.movies = newspaper_article.movies
            article.keywords = newspaper_article.keywords
            article.tags = list(newspaper_article.tags)

            article.authors = newspaper_article.authors

            if newspaper_article.publish_date:
                article.publish_date = newspaper_article.publish_date.replace(tzinfo=datetime.timezone.utc)

            article.summary = newspaper_article.summary

            meta_data = {key.replace('.', '_').replace('$', '__'): value for key, value in newspaper_article.summary}

            article.meta_data = meta_data

            article.language = newspaper_article.meta_lang

            article.text = newspaper_article.text
            article.html = newspaper_article.article_html

            article.save()

    logger.info('done with %s' % feed_url)
