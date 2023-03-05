class Board(object):

    __slots__ = ['_board1', '_board2']

    def __init__(self, board1, board2):
        self._board1 = board1
        self._board2 = board2

    @property
    def board1(self):
        return self._board1

    @property
    def board2(self):
        return self._board2


    def draw(self, board_suggest = None):
        board1 = self._board1.board
        board2 = self._board2.board
        print("\n" + "{:_<49}".format(""))
        for i in range(63, -1, -1):
            if (board1 >> i) & 1 == 1:
                print("{:1} {:^3}".format("|", "B"), end=' ')
            elif (board2 >> i) & 1 == 1:
                print("{:1} {:^3}".format("|", "W"), end=' ')
            elif board_suggest == None:
                print("{:1} {:^3}".format("|", " "), end=' ')
            else:
                if (board_suggest >> i) & 1 == 1:
                    print("{:1} {:^3}".format("|", "O"), end=' ')
                else:
                    print("{:1} {:^3}".format("|", " "), end=' ')
            if i % 8 == 0:
                print("{:1} {:2}".format("|", str(7 - i // 8)) + '\n' + "{:_<49}".format(""))
        rows = "ABCDEFGH"
        for i in rows:
            if i == "A":
                print("{:^1} {:^3}".format(" ", i), end=' ')
                continue
            print("{:^1} {:^3}".format("|", i), end=' ')