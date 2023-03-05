from maps.map import *

heuristics = [
    5, -4, 2, 2, 2, 2, -4, 5,
    -4, -5, -1, -1, -1, -1, -5, -4,
    2, -1, 2, 0, 0, 2, -1, 2,
    2, -1, 0, 1, 1, 0, -1, 2,
    2, -1, 0, 1, 1, 0, -1, 2,
    2, -1, 2, 0, 0, 2, -1, 2,
    -4, -5, -1, -1, -1, -1, -5, -4,
    5, -4, 2, 2, 2, 2, -4, 5
]

class State(object):

    __slots__ = ['_board', '_turn', '_column']

    def __init__(self, board, turn=None):
        self._board = board
        self._turn = turn
        self._column = self.create_columns()

    @property
    def board(self):
        return self._board

    @board.setter
    def board(self, board):
        self._board = board

    @property
    def turn(self):
        return self._turn

    @turn.setter
    def turn(self, turn):
        self._turn = turn

    @property
    def column(self):
        return self._column

    def create_columns(self):
        column = Map()
        column['A'] = 0
        column['B'] = 1
        column['C'] = 2
        column['D'] = 3
        column['E'] = 4
        column['F'] = 5
        column['G'] = 6
        column['H'] = 7
        return column
    
    def row_column(self, row, col):
        return 63 - 8*row - self.column[col]

    def set_field(self, row, column):
        n = self.row_column(row, column)
        self.board |= (1 << n)

    def get_field(self, row, column):
        n = self.row_column(row, column)
        # return 1 if it has something
        return self.board & (1 << n) > 0

    def with_move(self, move):
        return self.board | (1 << move)

    def score(self):
        counter = 0
        board = self.board
        for i in range(63,-1,-1):
            if not board > 0:
                break
            board &= board-1
            counter += 1
        return counter

    # def draw(self):
    #     print("\n" + "{:_<49}".format(""))
    #     for i in range(63, -1, -1):
    #         if (self.board >> i) & 1 == 1:
    #             print("{:1} {:^3}".format("|", "X"), end=' ')
    #         else:
    #             print("{:1} {:^3}".format("|", " "), end=' ')
    #         if i % 8 == 0:
    #             print("{:1} {:2}".format("|", str(7 - i // 8)) + '\n' + "{:_<49}".format(""))
    #     rows = "ABCDEFGH"
    #     for i in rows:
    #         if i == "A":
    #             print("{:^1} {:^3}".format(" ", i), end=' ')
    #             continue
    #         print("{:^1} {:^3}".format("|", i), end=' ')



