import unittest
import json

from tornado.web import HTTPError

from tictactoe import decorators as d
from tictactoe.models import User

from .helpers_decorators import (FakeGame, FakeRequest, FakeHandler,
                                 fake_method, assert_decorates)


class TestDecorators(unittest.TestCase):
    def test_authenticated(self):
        fake_handler = FakeHandler(current_user=User('test'))
        assert_decorates(d.authenticated, fake_handler)

    def test_authenticated_raise(self):
        fake_handler = FakeHandler(current_user=None)
        decorated = d.authenticated(fake_method)
        with self.assertRaises(HTTPError):
            decorated(fake_handler)

    def test_parse_json_request_with_data(self):
        request_data = {'key': 'value'}
        fake_handler = FakeHandler(
            request=FakeRequest(body=json.dumps(request_data)))

        assert_decorates(d.parse_json_request, fake_handler)
        assert fake_handler.req_data == request_data

    def test_parse_json_request_without_data(self):
        fake_handler = FakeHandler(request=FakeRequest(body=None))

        assert_decorates(d.parse_json_request, fake_handler)
        assert fake_handler.req_data == {}

    def test_fetch_game_preset(self):
        fake_handler = FakeHandler()
        fake_game = 'game'
        fake_handler.storage.save('game', 1, fake_game)
        assert_decorates(d.fetch_game, fake_handler, in_args=(1,), out_args=())
        assert fake_handler.game == fake_game

    def test_fetch_game_missing(self):
        fake_handler = FakeHandler()
        decorated = d.fetch_game(fake_method)
        with self.assertRaises(HTTPError):
            decorated(fake_handler, 1)

    def test_save_game(self):
        fake_game = FakeGame()
        fake_handler = FakeHandler(game=fake_game)
        assert_decorates(d.save_game, fake_handler)
        assert fake_handler.storage.find('game', fake_game.uid) == fake_game

    def test_respond_with_game(self):
        fake_game = FakeGame()
        fake_handler = FakeHandler(game=fake_game)
        assert_decorates(d.respond_with_game, fake_handler)
        assert fake_handler.output == fake_game.to_dict()
