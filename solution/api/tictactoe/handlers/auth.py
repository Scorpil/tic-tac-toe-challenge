import os
import jwt
import tornado

from ..models import User
from ..decorators import parse_json_request

SECRET = os.environ.get('SECRET')


class AuthHandler(tornado.web.RequestHandler):
    @parse_json_request
    def post(self):
        if not self.req_data.get('name'):
            raise tornado.web.HTTPError(status_code=400,
                                        reason="Name missing")
        user = User(self.req_data['name'])
        token = jwt.encode(user.to_dict(), SECRET, algorithm='HS256')
        self.write({'token': token.decode('utf-8')})
