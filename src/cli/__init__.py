import logging
import mongoengine

from .. import app
from src.models import User, Article, Feed, Vote, D2VModel

from src.ml.update_db import update_db
from src.ml.vectorize import vectorize

import sys

import click
from flask.cli import with_appcontext

logger = logging.getLogger(__name__)


@app.cli.command()
def fetch_feeds():
    logger.info('starting updatedb')
    update_db()
    logger.info('done with updatedb')
    logger.info('re-learning...')
    model = vectorize()
    Article.update_vectors(model)


@app.cli.command()
def clean_feeds():
    """delete unused feeds"""
    unused_feeds = Feed.objects(users=[])
    print('deleting %s' % [f.url for f in unused_feeds])
    unused_feeds.delete()
    for a in Article.objects:
        try:
            a.feed
        except mongoengine.errors.DoesNotExist:
            a.delete()


@app.cli.command()
def learn():
    logger.info('re-train doc2vec')
    vectorize()
    logger.info('done!')


@app.cli.command()
def flush_db():
    """flush the database."""
    User.objects.all().delete()
    Article.objects.all().delete()
    Feed.objects.all().delete()
    Vote.objects.all().delete()


@app.cli.command()
def flush_articles():
    Article.objects.all().delete()

@app.cli.command()
def flush_d2vmodel():
    D2VModel.objects.all().delete()


@app.cli.command()
def stats():
    for feed in Feed.objects:
        print('%s - %s' % (feed.title, Article.objects(feed=feed).count()))


@app.cli.command()
@click.argument('text')
def find_similar(text):
    from src.models import Article
    from nltk.tokenize import word_tokenize
    from gensim.models.doc2vec import Doc2Vec

    model = Doc2Vec.load("d2v.model")

    test_data = word_tokenize(text.lower())
    v1 = model.infer_vector(test_data)

    similar_doc = model.docvecs.most_similar([v1])
    obj_id = similar_doc[0][0]
    print(type(similar_doc[0][0]))
    print(Article.objects(id=obj_id).first().text)
    return


# https://github.com/ei-grad/flask-shell-ipython/blob/master/flask_shell_ipython.py


@app.cli.command()
def ishell():
    """Runs a shell in the app context.
    Runs an interactive Python shell in the context of a given
    Flask application. The application will populate the default
    namespace of this shell according to it's configuration.
    This is useful for executing small snippets of management code
    without having to manually configuring the application.
    """
    import IPython
    from IPython.terminal.ipapp import load_default_config
    from traitlets.config.loader import Config
    from flask.globals import _app_ctx_stack

    app = _app_ctx_stack.top.app

    if 'IPYTHON_CONFIG' in app.config:
        config = Config(app.config['IPYTHON_CONFIG'])
    else:
        config = load_default_config()

    config.TerminalInteractiveShell.banner1 = '''Python %s on %s
IPython: %s
App: %s%s
Instance: %s''' % (sys.version,
                   sys.platform,
                   IPython.__version__,
                   app.import_name,
                   app.debug and ' [debug]' or '',
                   app.instance_path)

    IPython.start_ipython(
        argv=[],
        user_ns=app.make_shell_context(),
        config=config,
    )


@app.cli.command()
def plot():
    import matplotlib
    # Force matplotlib to not use any Xwindows backend.
    matplotlib.use('Agg')

    from sklearn.manifold import TSNE
    from src.ml.vectorize import vectorize
    from sklearn.decomposition import PCA
    from src.models import Article, Feed
    import matplotlib.pyplot as plt
    import matplotlib.cm as cm
    import numpy as np
    from nltk.tokenize import word_tokenize
    from gensim.models.doc2vec import Doc2Vec

    #doc2vec = vectorize()
    doc2vec = Doc2Vec.load('d2v.model')

    all_docs = Article.objects.all()

    all_texts = {'%s_%s' % (idx, doc.title): dict(text=doc.text, source=doc.feed.title) for idx, doc in
                 enumerate(all_docs)}

    docs = [{'source': v['source'],
             'vec': doc2vec.infer_vector(word_tokenize(v['text']))} for title, v in
            all_texts.items()]
    pca = PCA(n_components=50)

    fiftyDimVecs = pca.fit_transform([doc['vec'] for doc in docs])
    tsne = TSNE(n_components=2)

    twoDimVecs = tsne.fit_transform(fiftyDimVecs)
    print(list(twoDimVecs))
    """
    colors = cm.rainbow(np.linspace(0, 1, Feed.objects.count()))
    feeds = Feed.objects
    feed_colors = {feed.title: colors[idx] for idx, feed in enumerate(feeds)}

    subplots = {source: plt.subplot() for source in feed_colors.keys()}

    for doc, twoDimVec in zip(docs, twoDimVecs):
        subplots[doc['source']].scatter(twoDimVec[0], twoDimVec[1], color=(feed_colors[doc['source']]))

    keys, values = zip(*subplots.items())
    print(keys)
    print(values)
    plt.legend(values,
               keys,
               loc='lower left',
             )

    plt.savefig('plot.png')
    """
