from flask_restful import Resource

from flask_login import login_required, current_user

from src.models import User
from flask import request, abort


class TokenView(Resource):
    method_decorators = {
        'get': [login_required],
        'post': [login_required]

    }

    def get(self):
        token = current_user.generate_auth_token()
        return {'token': token.decode('ascii')}
