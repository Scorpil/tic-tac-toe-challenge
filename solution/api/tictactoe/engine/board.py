class Board:
    BOARD_SIDE_LEN = 3
    WIN_LINES = [
        # horizontal
        [0, 1, 2],
        [3, 4, 5],
        [6, 7, 8],
        # vertical
        [0, 3, 6],
        [1, 4, 7],
        [2, 5, 8],
        # diagonal
        [0, 4, 8],
        [2, 4, 6],
    ]

    def __init__(self, history=None):
        self.winner = None
        self.cells = [None] * self.num_cells
        self.history = []
        for move in (history or []):
            self.mark_move(move)

    def mark_move(self, cell_id):
        if self.is_finished:
            raise RuntimeError('The game has ended')
        if self.cells[cell_id] is not None:
            raise ValueError('Illegal move')
        self.cells[cell_id] = self.next_symbol_id
        self.history.append(cell_id)

        if self.is_winning_move(cell_id):
            self.winner = self.cells[cell_id]

    def is_winning_move(self, modified_cell_id):
        """
        Returns True if updating `modified_cell_id` has led to win condition
        """
        if self.num_moves < 5:
            # winning sooner than move 5 if not possible
            return False
        for line in self.WIN_LINES:
            if modified_cell_id in line and \
               self._is_line_complete(line, self.cells[modified_cell_id]):
                return True
        return False

    def _is_line_complete(self, line, value):
        """
        Returns True if all cells given by their id's in `line` contain `value`
        """
        for cell_id in line:
            if self.cells[cell_id] != value:
                return False
        return True

    @property
    def next_symbol_id(self):
        """
        Returns `symbol_id` for the next move

        Since symbol_id jumps between 0 and 1 after each turn,
        it will always be 0 for even turns (starting from turn 0),
        and 1 for odd turns
        """
        return self.num_moves % 2

    @property
    def num_moves(self):
        return len(self.history)

    @property
    def num_cells(self):
        return self.BOARD_SIDE_LEN * self.BOARD_SIDE_LEN

    @property
    def is_finished(self):
        return self.winner is not None or self.num_moves == self.num_cells
