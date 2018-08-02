from flask_restful import Resource
from flask import make_response, Response, stream_with_context

from flask_login import login_required
from src.models import Article, D2VModel


from marshmallow import Schema, fields


def make_octet_response(model, code, headers=None):
    return Response(model.serialized_model, direct_passthrough=True)


class ModelView(Resource):
    class RssView(Resource):
        representations = {
            'application/octet-stream': make_octet_response,
        }
        method_decorators = {
            'get': [login_required],
        }

        def get(self):
            model = D2VModel.get()
            return model

