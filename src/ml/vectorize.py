
import nltk
from src.models import Article

from gensim.models.doc2vec import Doc2Vec, TaggedDocument
from nltk.tokenize import word_tokenize



def vectorize():

    nltk.download('punkt')

    all_docs = Article.objects.all()
    all_texts = {doc.id: doc.text for doc in all_docs}

    tagged_data = [TaggedDocument(words=word_tokenize(doc.lower()), tags=[id]) for id, doc in all_texts.items()]

    vec_size = 50
    alpha = 0.025

    model = Doc2Vec(vector_size=vec_size,
                    alpha=alpha,
                    min_alpha=0.00025,
                    min_count=2,
                    epochs=40)

    model.build_vocab(tagged_data)

    model.train(tagged_data, total_examples=model.corpus_count, epochs=model.epochs)

    model.save("d2v.model")
    return model

