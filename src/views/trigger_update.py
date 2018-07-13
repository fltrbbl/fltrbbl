from flask_restful import Resource

from flask_login import login_required, current_user

from src.ml.update_db import update_db

from src.models import Feed, User
from flask import request, abort



class TriggerUpdateView(Resource):
    method_decorators = {
        'get': [login_required],
        'post': [login_required]
    }

    def get(self):
        # todo: filter orphan feeds

        update_db()
        return {}, 200
