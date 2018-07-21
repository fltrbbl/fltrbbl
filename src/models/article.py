from pymongo import UpdateOne

from src import db
from .feed import Feed


class Article(db.Document):
    feed = db.ReferenceField(Feed, required=True)
    source_id = db.StringField(required=True)
    url = db.StringField()

    title = db.StringField()
    top_image = db.StringField()
    movies = db.ListField()
    keywords = db.ListField()
    tags = db.ListField()
    authors = db.ListField()
    publish_date = db.DateTimeField()
    summary = db.StringField()
    html = db.StringField()
    meta_data = db.DictField()

    language = db.StringField()

    text = db.StringField()
    active = db.BooleanField(default=True)

    vector = db.ListField(db.FloatField())

    def as_dict(self):
        return dict(
            feed=self.feed.url,
            source_id=self.source_id,
            url=self.url,
            title=self.title,
            top_image=self.top_image,
            movies=self.movies,
            keywords=self.keywords,
            tags=self.tags,
            authors=self.authors,
            publish_date='%s' % self.publish_date,
            summary=self.summary,
            html=self.html,
            meta_data=self.meta_data,
            language=self.language,
            text=self.text,
            vector=self.vector
        )

    @staticmethod
    def update_vectors(model):
        # https://stackoverflow.com/questions/30943076/mongoengine-bulk-update-without-objects-update
        bulk_operations = []

        keys = model.docvecs.doctags.keys()
        vectors = model.docvecs.vectors_docs

        for key, vector in zip(keys, vectors):
            bulk_operations.append(
                UpdateOne({'_id': key}, {'$set': dict(vector=vector.tolist())}))

        if bulk_operations:
            collection = Article._get_collection() \
                .bulk_write(bulk_operations, ordered=False)
