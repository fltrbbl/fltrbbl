import matplotlib
# Force matplotlib to not use any Xwindows backend.
matplotlib.use('Agg')

from sklearn.manifold import TSNE
from sklearn.decomposition import PCA
from src.models import Article, Feed, D2VModel
from nltk.tokenize import word_tokenize


import nltk


def update_plotable():
    nltk.download('punkt')

    db_model = D2VModel.get()
    model = db_model.model

    articles = Article.objects.only('title', 'feed', 'url', 'id', 'text').all()
    vectors = []
    for article in articles:
        vectors.append(model.infer_vector(word_tokenize(article.text.lower())))

    pca = PCA(n_components=50)

    fiftyDimVecs = pca.fit_transform(vectors)
    tsne = TSNE(n_components=2)

    twoDimVecs = tsne.fit_transform(fiftyDimVecs)
    serializable_twoDimVecs = [vec.tolist() for vec in twoDimVecs]

    articles_with_vectors = []
    for article, vector in zip(articles, serializable_twoDimVecs):
        articles_with_vectors.append(article.to_json().update({'vector': vector}))

    return articles_with_vectors, 200
