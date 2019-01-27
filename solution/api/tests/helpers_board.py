from tictactoe.engine.board import Board


N = None


def win_lines():
    return [
        [0, 1, 2],
        [3, 4, 5],
        [6, 7, 8],
        [0, 3, 6],
        [1, 4, 7],
        [2, 5, 8],
        [0, 4, 8],
        [2, 4, 6],
    ]


def win_board_horiz_0():
    board = Board([])
    board.cells = [0, 0, 0,
                   1, 0, 1,
                   N, N, 1]
    return (board, [0, 1, 2], 0)


def win_board_diag_1():
    board = Board([])
    board.cells = [1, 0, 0,
                   N, 1, 1,
                   N, N, 1]
    return (board, [0, 4, 8], 1)


def win_board_diag_0():
    board = Board([])
    board.cells = [1, 0, 0,
                   1, 0, 1,
                   0, 1, 1]
    return (board, [2, 4, 6], 0)


def win_boards():
    return [win_board_horiz_0(), win_board_diag_1()]


def story_fast_game():
    return [[
        (4, [N, N, N,
             N, 0, N,
             N, N, N]),
        (0, [1, N, N,
             N, 0, N,
             N, N, N]),
        (2, [1, N, 0,
             N, 0, N,
             N, N, N]),
        (6, [1, N, 0,
             N, 0, N,
             1, N, N]),
        (5, [1, N, 0,
             N, 0, 0,
             1, N, N]),
        (3, [1, N, 0,
             1, 0, 0,
             1, N, N])], 1]


def story_long_game():
    return [[
        (0, [0, N, N,
             N, N, N,
             N, N, N]),
        (8, [0, N, N,
             N, N, N,
             N, N, 1]),
        (2, [0, N, 0,
             N, N, N,
             N, N, 1]),
        (1, [0, 1, 0,
             N, N, N,
             N, N, 1]),
        (4, [0, 1, 0,
             N, 0, N,
             N, N, 1]),
        (7, [0, 1, 0,
             N, 0, N,
             N, 1, 1]),
        (5, [0, 1, 0,
             N, 0, 0,
             N, 1, 1]),
        (3, [0, 1, 0,
             1, 0, 0,
             N, 1, 1]),
        (6, [0, 1, 0,
             1, 0, 0,
             0, 1, 1]),
    ], 0]


def story_draw():
    return [[
        (0, [0, N, N,
             N, N, N,
             N, N, N]),
        (8, [0, N, N,
             N, N, N,
             N, N, 1]),
        (2, [0, N, 0,
             N, N, N,
             N, N, 1]),
        (1, [0, 1, 0,
             N, N, N,
             N, N, 1]),
        (7, [0, 1, 0,
             N, N, N,
             N, 0, 1]),
        (6, [0, 1, 0,
             N, N, N,
             1, 0, 1]),
        (5, [0, 1, 0,
             N, N, 0,
             1, 0, 1]),
        (4, [0, 1, 0,
             N, 1, 0,
             1, 0, 1]),
        (3, [0, 1, 0,
             0, 1, 0,
             1, 0, 1]),
    ], None]


def stories():
    return [story_fast_game(), story_long_game(), story_draw()]
