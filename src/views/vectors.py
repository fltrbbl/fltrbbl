from flask_restful import Resource

from flask_login import login_required, current_user
from gensim.models.doc2vec import Doc2Vec, TaggedDocument
from src.ml.transform_2d import update_plotable
from src.models import D2VModel


class VectorsView(Resource):
    method_decorators = {
        'get': [login_required],
        'post': [login_required]
    }

    def get(self):
        return update_plotable()
