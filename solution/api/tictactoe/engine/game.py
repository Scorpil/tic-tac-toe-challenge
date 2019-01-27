from uuid import uuid4
import tornado

from .board import Board


class PlayerValueError(ValueError):
    pass


class MoveValueError(ValueError):
    pass


class Game:
    MAX_PLAYERS = 2

    STATE_MATCHMAKING = 'matchmaking'
    STATE_IN_PROGRESS = 'in_progress'
    STATE_FINISHED = 'finished'

    def __init__(self, players, uid=None, board=None):
        self.uid = str(uuid4())
        self.players = players

        self.board = board or Board()

    def join(self, player):
        if len(self.players) >= self.MAX_PLAYERS:
            raise RuntimeError('Game is full')
        self.players.append(player)

    def make_move(self, player, move):
        if player != self.next_player:
            raise PlayerValueError('Wrong player')
        try:
            self.board.mark_move(move)
        except ValueError as e:
            raise MoveValueError(e)

    @property
    def state(self):
        if len(self.players) < self.MAX_PLAYERS:
            return self.STATE_MATCHMAKING
        if self.board.is_finished:
            return self.STATE_FINISHED
        return self.STATE_IN_PROGRESS

    @property
    def winner(self):
        if self.board.winner is None:
            return None
        return self.players[self.board.winner].name

    @property
    def moves(self):
        return self.board.history

    @property
    def next_player(self):
        return self.players[self.board.next_symbol_id]

    def to_dict(self):
        return {
            'id': self.uid,
            'players': [player.name for player in self.players],
            'state': self.state,
            'moves': self.moves,
            'winner': self.winner,
        }

    def __repr__(self):
        return f'[ Game | id = {self.uid} ]'
