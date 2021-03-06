from flask_restful import Resource

from flask_login import login_required
from src.models import Article


from marshmallow import Schema, fields

class FeedSchema(Schema):
    id = fields.Str()

class ArticleVectorSchema(Schema):
    feed = fields.Nested(FeedSchema)

    url = fields.Str()
    title = fields.Str()
    vector = fields.List(fields.Float())
    publish_date = fields.DateTime()
    vector_2d = fields.List(fields.Float())



class VectorsView(Resource):
    method_decorators = {
        'get': [login_required],
        'post': [login_required]
    }

    def get(self):
        articles = Article.objects.only(
            'feed', 'url', 'title', 'vector', 'publish_date', 'vector_2d')
        article_schema = ArticleVectorSchema()

        return article_schema.dump(articles, many=True)
