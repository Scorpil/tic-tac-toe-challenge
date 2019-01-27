from tornado.web import HTTPError

from .base import BaseRequestHandler
from ..engine import Game, PlayerValueError, MoveValueError
from ..decorators import (authenticated, parse_json_request,
                          fetch_game, save_game, respond_with_game)


class GameHandler(BaseRequestHandler):
    @fetch_game
    @respond_with_game
    def get(self): pass

    @authenticated
    @parse_json_request
    @fetch_game
    @save_game
    @respond_with_game
    def post(self):
        if self.game.state == Game.STATE_MATCHMAKING:
            return self._join_game()
        return self._make_move()

    def _join_game(self):
        players = self.game.to_dict()['players']
        players.append(self.current_user.name)
        if self.req_data.get('players') != players:
            raise HTTPError(400)
        self.game.join(self.current_user)

    def _make_move(self):
        if self.req_data.get('players') != self.game.to_dict()['players'] or \
           len(self.req_data['moves']) != (len(self.game.moves) + 1) or \
           self.req_data['moves'][:-1] != self.game.moves:
            raise HTTPError(400)

        move = self.req_data['moves'][-1]
        try:
            self.game.make_move(self.current_user, move)
        except PlayerValueError as e:
            raise HTTPError(409, reason=str(e))
        except MoveValueError as e:
            raise HTTPError(400, reason=str(e))
