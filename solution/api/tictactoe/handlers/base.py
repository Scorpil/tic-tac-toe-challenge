import os
import jwt
import tornado

from ..models import User


SECRET = os.environ.get('SECRET')


class BaseRequestHandler(tornado.web.RequestHandler):
    def initialize(self, storage):
        self.storage = storage

    def get_current_user(self):
        auth_header = self.request.headers.get('Authorization')
        if not auth_header:
            return None

        try:
            (auth_type, token) = auth_header.split(' ')
        except ValueError:
            return None

        if auth_type.lower() != 'bearer':
            return None

        jwt_data = jwt.decode(token.encode('utf-8'), SECRET,
                              algorithms=['HS256'])
        return User.from_dict(jwt_data)
