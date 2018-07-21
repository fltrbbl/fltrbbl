import io
import nltk
from src.models import Article, D2VModel

from gensim.models.doc2vec import Doc2Vec, TaggedDocument
from nltk.tokenize import word_tokenize
from typing import List


def vectorize():
    nltk.download('punkt')

    all_docs: List[Article] = Article.objects.all()

    tagged_data = [TaggedDocument(words=word_tokenize(doc.text.lower()),
                                  tags=[doc.id]) for doc
                   in all_docs]
    vec_size = 50
    alpha = 0.025

    model = Doc2Vec(vector_size=vec_size,
                    alpha=alpha,
                    min_alpha=0.00025,
                    min_count=2,
                    epochs=40)

    model.build_vocab(tagged_data)

    model.train(tagged_data, total_examples=model.corpus_count, epochs=model.epochs)

    db_model = D2VModel.get()
    db_model.model = model
    db_model.save()
    return model
