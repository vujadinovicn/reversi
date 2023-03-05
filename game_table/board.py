class Board(object):

    __slots__ = ['_black_state', '_white_state']

    def __init__(self, black_state, white_state):
        self._black_state = black_state
        self._white_state = white_state

    @property
    def black_state(self):
        return self._black_state

    @property
    def white_state(self):
        return self._white_state

    def draw(self, board_suggest = None):
        self.draw_first_row_line()
        self.draw_all_fields(board_suggest)
        self.draw_column_names()

    def draw_first_row_line():
        print("\n" + "{:+<49}".format(""))

    def draw_all_fields(self, board_suggest):
        for i in range(63, -1, -1):
            self.draw_field(board_suggest, i)
            self.draw_row_number_and_line(i)

    def draw_field(self, board_suggest, i):
        black_board = self._black_state.board
        white_board = self._white_state.board
        if (black_board >> i) & 1 == 1:
            self.fill_field_with_letter("B")
        elif (white_board >> i) & 1 == 1:
            self.fill_field_with_letter("W")
        elif board_suggest == None:
            self.fill_field_with_letter(" ")
        else:
            self.draw_suggestion(board_suggest, i)

    def fill_field_with_letter(self, field_letter):
         print("{:1} {:^3}".format("|", field_letter), end=' ')

    def draw_suggestion(self, board_suggest, i):
        if (board_suggest >> i) & 1 == 1:
            self.fill_field_with_letter("0")
        else:
            self.fill_field_with_letter(" ")

    def draw_row_number_and_line(self, i):
        if i % 8 == 0:
                print("{:1} {:2}".format("|", str(7 - i // 8)) + '\n' + "{:_<49}".format(""))

    def draw_column_names(self): 
        rows = "ABCDEFGH"
        for i in rows:
            if i == "A":
                print("{:^1} {:^3}".format(" ", i), end=' ')
                continue
            print("{:^1} {:^3}".format("|", i), end=' ')