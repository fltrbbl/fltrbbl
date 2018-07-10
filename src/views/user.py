from flask_restful import Resource

from flask_login import login_required, current_user

from src.models import User
from flask import request, abort


class UserView(Resource):
    method_decorators = {
        'get': [login_required],
        'post': [login_required]
    }

    def get(self):
        return current_user.as_dict(), 200

    def put(self):
        email = request.json.get('email')
        password = request.json.get('password')

        if email is None or password is None:
            abort(400)  # missing arguments
        if User.objects(email=email).first() is not None:
            abort(400)  # existing user

        user = User(email=email)
        user.hash_password(password)
        user.save()

        return user.as_dict(), 201
