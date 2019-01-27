import os
from tornado.web import Application

from .handlers import GameRepoHandler, GameHandler, AuthHandler
from .storage import Storage


def make_app():
    storage = Storage()
    return Application([
        (r"/api/auth", AuthHandler),
        (r"/api/games", GameRepoHandler, dict(storage=storage)),
        (r"/api/games/([-a-z0-9]{36})", GameHandler, dict(storage=storage)),
    ], debug=(os.environ.get('DEBUG') == '1'))
