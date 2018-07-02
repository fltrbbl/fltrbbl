from .. import admin
from .. import db
from ..models import *

from .base import BaseView

admin.add_view(BaseView(User, db.session))
admin.add_view(BaseView(Article, db.session))
admin.add_view(BaseView(Feed, db.session))

