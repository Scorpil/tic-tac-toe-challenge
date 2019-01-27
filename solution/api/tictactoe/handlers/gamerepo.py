from .base import BaseRequestHandler
from ..engine import Game
from ..decorators import (authenticated, parse_json_request,
                          save_game, respond_with_game)


class GameRepoHandler(BaseRequestHandler):
    def get(self):
        self.write({
            'items': [game.to_dict() for game in self.storage.find_all('game')]
        })

    @authenticated
    @parse_json_request
    @save_game
    @respond_with_game
    def post(self):
        self.game = Game([self.current_user])
