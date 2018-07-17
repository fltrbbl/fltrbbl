from flask_restful import Resource

from flask_login import login_required, current_user
from gensim.models.doc2vec import Doc2Vec, TaggedDocument
from src.ml.vectorize import vectorize


class VectorsView(Resource):
    method_decorators = {
        'get': [login_required],
        'post': [login_required]
    }

    def get(self):
        import matplotlib
        # Force matplotlib to not use any Xwindows backend.
        matplotlib.use('Agg')

        from sklearn.manifold import TSNE
        from sklearn.decomposition import PCA
        from src.models import Article, Feed
        from nltk.tokenize import word_tokenize
        from gensim.models.doc2vec import Doc2Vec

        # doc2vec = vectorize()
        model = Doc2Vec.load('d2v.model')

        keys = list(model.docvecs.doctags.keys())

        vectors = model.docvecs.vectors_docs

        pca = PCA(n_components=50)

        fiftyDimVecs = pca.fit_transform(vectors)
        tsne = TSNE(n_components=2)

        twoDimVecs = tsne.fit_transform(fiftyDimVecs)
        serializable_twoDimVecs = [vec.tolist() for vec in twoDimVecs]

        return dict(keys=keys, vectors=serializable_twoDimVecs), 200
