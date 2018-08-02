import io
import datetime
import pickle

from src import db


class D2VModel(db.Document):
    serialized_model = db.FileField()
    last_run = db.DateTimeField()

    vectors = db.DictField()

    # [
    #   [a1, a2],
    #   [b1, b2]
    # ]
    vectors_2d = db.ListField(db.ListField(db.FloatField()))

    @property
    def model(self):
        """
        load serialized model

        :return:
        """
        if not self.serialized_model:
            return None

        bytes_io = io.BytesIO(self.serialized_model)
        model = pickle.load(bytes_io)
        return model

    @model.setter
    def model(self, model):
        # instead of a file
        bytes_io = io.BytesIO()

        # save model to bytesio
        model.save(bytes_io)

        # getvalue has the actual bytes
        self.serialized_model = bytes_io.getvalue()

        # close buffer
        bytes_io.close()

        # update timestamp and save
        self.touch()


    @staticmethod
    def get():
        d2v_model = D2VModel.objects.first()
        if not d2v_model:
            d2v_model = D2VModel()
            d2v_model.touch()
            d2v_model.save()
        return d2v_model


    def touch(self):
        self.last_run = datetime.datetime.now()
