from json.decoder import JSONDecodeError

from tornado.escape import json_decode
from tornado.web import HTTPError


def authenticated(method):
    def wrapper(self, *args, **kwargs):
        if not self.current_user:
            raise HTTPError(403)
        return method(self, *args, **kwargs)
    return wrapper


def parse_json_request(method):
    def wrapper(self, *args, **kwargs):
        if not self.request.body:
            # allow empty body
            self.req_data = {}
        else:
            try:
                self.req_data = json_decode(self.request.body)
            except JSONDecodeError:
                raise HTTPError(400)

        return method(self, *args, **kwargs)
    return wrapper


def fetch_game(method):
    """
    Helper decorator that fetches game istance base on game_id from url match
    """
    def wrapper(self, game_id, *args, **kwargs):
        try:
            self.game = self.storage.find('game', game_id)
        except KeyError:
            raise HTTPError(404)
        return method(self, *args, **kwargs)
    return wrapper


def save_game(method):
    """
    Helper decorator that saves modifications to the game
    when handler has finished execution
    """
    def wrapper(self, *args, **kwargs):
        result = method(self, *args, **kwargs)
        self.storage.save('game', self.game.uid, self.game)
        return result
    return wrapper


def respond_with_game(method):
    """
    Helper decorator that writes a response based on game instance
    """
    def wrapper(self, *args, **kwargs):
        result = method(self, *args, **kwargs)
        self.write(self.game.to_dict())
        return result
    return wrapper
