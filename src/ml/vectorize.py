import io
import nltk
from src.models import Article, D2VModel

from gensim.models.doc2vec import Doc2Vec, TaggedDocument
from nltk.tokenize import word_tokenize
from typing import List

import matplotlib

# Force matplotlib to not use any Xwindows backend.
matplotlib.use('Agg')

from sklearn.manifold import TSNE
from sklearn.decomposition import PCA
from src.models import Article, Feed
from nltk.tokenize import word_tokenize
from gensim.models.doc2vec import Doc2Vec


def train_model(all_docs, vec_size=50, alpha = 0.025, min_alpha=0.00025, min_count=2, epochs=40):
    tagged_data = [TaggedDocument(words=word_tokenize(doc.text.lower()),
                                  tags=[doc.id]) for doc
                   in all_docs]

    model = Doc2Vec(vector_size=vec_size,
                    alpha=alpha,
                    min_alpha=min_alpha,
                    min_count=min_count,
                    epochs=epochs)

    model.build_vocab(tagged_data)

    model.train(tagged_data, total_examples=model.corpus_count, epochs=model.epochs)
    return model


def vectorize():
    nltk.download('punkt')

    all_docs: List[Article] = Article.objects.all()

    model = train_model(all_docs)

    vectors_2d = build_2d_vecs(model)

    db_model = D2VModel.get()
    db_model.model = model
    db_model.vectors_2d = vectors_2d
    db_model.save()
    return model, vectors_2d


def build_2d_vecs(model):
    vectors = model.docvecs.vectors_docs

    pca = PCA(n_components=50)

    fiftyDimVecs = pca.fit_transform(vectors)
    tsne = TSNE(n_components=2)

    two_dim_vectors = tsne.fit_transform(fiftyDimVecs)

    serializable_two_dim_vectors = [vec.tolist() for vec in two_dim_vectors]

    return serializable_two_dim_vectors
