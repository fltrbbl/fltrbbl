import logging

from .. import app
from src.models import User, Article, Feed, Vote

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
    logger.info('starting updatedb')


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
def stats():
    for feed in Feed.objects:
        print('%s - %s' % (feed.title, Article.objects(feed=feed).count()))

@app.cli.command()
@click.argument('text')
def find_similar(text):
    from src.models import Article
    from nltk.tokenize import word_tokenize
    from gensim.models.doc2vec import Doc2Vec

    model= Doc2Vec.load("d2v.model")

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