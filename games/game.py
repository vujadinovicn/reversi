from trees.tree import Tree
from trees.tree_node import TreeNode
from maps.hash_map import ChainedHashMap
from game_table.board import Board
from game_table.state import State, heuristics
from games.constants import *


class Game(object):

    def __init__(self):
        black = State(BLACK_BOARD, "black")
        white = State(WHITE_BOARD, "white")
        hash_map = ChainedHashMap()
        self.play(black, white, hash_map)

    def up(self, board):
        return board << 8

    def down(self, board):
        return board >> 8

    def right(self, board):
        return (board & ~RIGHT) >> 1

    def left(self, board):
        return (board & ~LEFT) << 1

    def up_left(self, board):
        board_left = self.left(board)
        return self.up(board_left)

    def up_right(self, board):
        board_right = self.right(board)
        return self.up(board_right)

    def down_left(self, board):
        board_left = self.left(board)
        return self.down(board_left)

    def down_right(self, board):
        board_right = self.right(board)
        return self.down(board_right)


    def move(self, player_board, opponent_board, empty, possible, function):
        next_to = function(player_board) & opponent_board
        var = 0
        while next_to != var:
            var = next_to
            next_to |= function(next_to) & opponent_board
        possible |= function(next_to) & empty
        return possible


    def possible_moves(self, player, opponent):
        player_board = player.board
        opponent_board = opponent.board
        possible = 0
        empty = ~(player_board | opponent_board)

        functions = [self.up, self.up_right, self.up_left, self.down, self.down_right, self.down_left, self.right,
                     self.left]

        for function in functions:
            possible = self.move(player_board, opponent_board, empty, possible, function)
        return possible


    def flip_move(self, player_board, opponent_board, move, function):
        next_to = function(move) & opponent_board
        var = 0

        while next_to != var:
            var = next_to
            next_to |= function(next_to) & opponent_board
        if var > 0 and ((function(next_to) & player_board) != 0):
            if (function == self.up and var & UP == 0) or \
                    ((
                             function == self.right or function == self.up_right or function == self.down_right) and var & RIGHT == 0) or \
                    ((
                             function == self.left or function == self.up_left or function == self.down_left) and var & LEFT == 0) or \
                    (function == self.down and var & DOWN == 0):
                player_board |= next_to
                opponent_board &= ~next_to

        return player_board, opponent_board


    def flip(self, player, opponent, move):
        player_board = player.board | move
        opponent_board = opponent.board

        functions = [self.up, self.up_right, self.up_left, self.down, self.down_right, self.down_left, self.right,
                     self.left]

        for function in functions:
            player_board, opponent_board = self.flip_move(player_board, opponent_board, move, function)

        return player_board, opponent_board


    def legal_move(self, board, row, column):
        state = State(board, 'nobody')
        return state.get_field(row, column)


    def possible_children(self, player, opponent):
        possible = self.possible_moves(player, opponent)
        children = []
        for i in range(63, -1, -1):
            if possible & (1 << i) > 0:
                player_board, opponent_board = self.flip(player, opponent, (1 << i))
                state_player = State(player_board)
                state_opponent = State(opponent_board)
                children.append((state_player, state_opponent))
        return children


    def ai(self, player, opponent, hash_map):
        tree = Tree()
        tree.root = TreeNode((player, opponent))
        alpha = float('-inf')
        beta = float('+inf')
        v, pl, opp = self.minimax(tree.root, 3, alpha, beta, True, hash_map)
        return pl, opp


    def minimax(self, root, depth, alpha, beta, maximizer, hash_map):
        player, opponent = root.data[0], root.data[1]

        end, winner, type = self.over(player, opponent, "p")
        if end == True or depth == 0:
            return self.heuristic_score(root.data[0], root.data[1]), root.data[0], root.data[1]

        children = self.possible_children(player, opponent)
        for i in range(len(children)):
            data = (children[i][1], children[i][0])
            c = TreeNode(data)
            root.add_child(c)

        c1, c2 = None, None
        children = root.children

        if maximizer:
            max_heuristic = float('-inf')
            for child in children:
                player_child, opponent_child = child.data[0], child.data[1]
                board = Board(player_child, opponent_child)
                if board in hash_map:
                    heuristic = hash_map[child]
                else:
                    heuristic, pom, pom2 = self.minimax(child, depth - 1, alpha, beta, False, hash_map)
                    hash_map.add(board, heuristic)

                if max_heuristic < heuristic:
                    max_heuristic = heuristic
                    c1 = player_child
                    c2 = opponent_child

                if heuristic >= alpha:
                    alpha = heuristic
                if alpha >= beta:
                    break

            return max_heuristic, c1, c2
        else:
            min_heuristic = float('inf')
            for child in children:
                player_child, opponent_child = child.data[0], child.data[1]
                board = Board(player_child, opponent_child)
                if board in hash_map:
                    heuristic = hash_map[child]
                else:
                    heuristic, pom, pom2 = self.minimax(child, depth - 1, alpha, beta, True, hash_map)
                    hash_map.add(board, heuristic)

                if min_heuristic > heuristic:
                    min_heuristic = heuristic
                    c1 = player_child
                    c2 = opponent_child

                if heuristic <= beta:
                    beta = heuristic
                if alpha >= beta:
                    break

            return min_heuristic, c1, c2


    def human(self, player, opponent):
        board_possible = self.possible_moves(player, opponent)
        while True:
            column = input("\n\nPut letter of the column: ")
            while not column in ["A", "B", "C", "D", "E", "F", "G", "H"]:
                print("Error has appeared. Try again")
                column = input("Put the letter of the column: ")
            row = input("Put the number of the row: ")
            while not row in ['0', '1', '2', '3', '4', '5', '6', '7']:
                print("Error has appeared. Try again")
                row = input("Put the letter of the row: ")
            row = int(row)
            if not self.legal_move(board_possible, row, column):
                print("Your move is not possible. Try again")
            else:
                break

        move = 0
        n = player.row_column(row, column)
        move |= (1 << n)
        player.board, opponent.board = self.flip(player, opponent, move)
        #return row, column


    def end(self, m):
        move = m
        for i in range(63, -1, -1):
            if (move >> i) & 1 == 1:
                return False
        return True

    def op(self, player):
        if player == "white":
            return "black"
        return "white"


    def over(self, player, opponent, turn):
        if self.end(self.possible_moves(player, opponent)):
            if self.end(self.possible_moves(player, opponent)) and self.end(self.possible_moves(opponent, player)):
                if player.score() > opponent.score():
                    return True, turn, "No more moves for both players."
                elif opponent.score() > player.score():
                    return True, self.op(turn), "No more moves for both players."
                return True, None, "No more moves for both players."
            type = "No more moves for " + turn
            return True, self.op(turn), type
        return False, None, None


    def play(self, player, opponent, hash_map):
        turn = "black"
        board = Board(player, opponent)
        while True:
            if turn == "black":
                end, winner, type = self.over(player, opponent, turn)
                if end:
                    print('Game is OVER')
                    if winner == None:
                        print(type)
                        print("THE GAME IS TIED.")
                    else:
                        print(type)
                        print("THE WINNER IS: " + winner)
                    return
                print("\n"+"{: <20}".format("")+"USER TURN")
                board.draw(self.possible_moves(player, opponent))
                self.human(player, opponent)
                #player, opponent = self.ai(player, opponent, hash_map)
                print("\n\n"+"{: <13}".format("")+"---------SCORE---------")
                print("{: <13}".format("")+" BLACK: ", player.score(), "  "+ "WHITE: ", opponent.score())
                board = Board(player, opponent)
                board.draw()
                turn = "white"
                print("\n")
            else:
                end, winner, type = self.over(opponent, player, turn)
                if end:
                    print('Game is OVER')
                    if winner == None:
                        print(type)
                        print("THE GAME IS TIED.")
                    else:
                        print(type)
                        print("THE WINNER IS: " + winner)
                    return
                print("\n"+"{: <20}".format("")+"COMPUTER TURN")
                #start = time.time()
                player, opponent = self.ai(opponent, player, hash_map)
                #Board(player, opponent).draw()
                #print(time.time() - start)
                board = Board(player, opponent)
                board.draw()
                print("\n\n" + "{: <13}".format("") + "---------SCORE---------")
                print("{: <13}".format("") + " BLACK: ", player.score(), "  " + "WHITE: ", opponent.score())
                turn = "black"

    def heuristic_score(self, player, opponent):
        score = 0
        player_board = player.board
        opponent_board = opponent.board
        possible_player = self.possible_moves(player, opponent)
        possible_opponent = self.possible_moves(opponent, player)
        for i in range(63, -1, -1):
            if (player_board >> i) & 1 == 1:
                score += heuristics[63 - i]
            if (opponent_board >> i) & 1 == 1:
                score -= heuristics[63 - i]
            if (possible_player >> i) & 1 == 1:
                score += 10
            if (possible_opponent >> i) & 1 == 1:
                score -= 5
            score += 2 * (player.score() - opponent.score())
            #score += 10*(player.score() - opponent.score())
        return score