import pytest
from tictactoe.engine.board import Board
from .helpers_board import win_lines, win_boards, stories, N


class TestBoard:
    def test_init_empty(self):
        empty_board = Board()
        assert empty_board.cells == [None] * 9
        assert len(empty_board.history) == 0

    def test_init_center_move(self):
        center_move_board = Board([4])
        assert center_move_board.cells == [N, N, N,
                                           N, 0, N,
                                           N, N, N]
        assert len(center_move_board.history) == 1

    @pytest.mark.parametrize('line', win_lines())
    @pytest.mark.parametrize('symbol_id', [0, 1])
    @pytest.mark.parametrize('board, win_line, win_symbol_id', win_boards())
    def test__is_line_complete(self, line, symbol_id,
                               board, win_line, win_symbol_id):
        expected_win = line == win_line and symbol_id == win_symbol_id
        is_win = board._is_line_complete(line, symbol_id)
        assert is_win == expected_win

    @pytest.mark.parametrize('story, winner', stories())
    def test_story(self, story, winner):
        board = Board()
        for (expected_num_moves,
             (move, expected_cells)) in enumerate(story, 1):
            board.mark_move(move)

            assert board.cells == expected_cells
            print(board.cells)
            assert len(board.history) == expected_num_moves
        assert board.winner == winner
