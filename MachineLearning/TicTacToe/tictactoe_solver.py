from MachineLearning.TicTacToe.tictactoe import Game  # if executing from directory root
#from tictactoe import Game  # if executing from current directory

import random
from math import inf
from copy import deepcopy


def print_board(board):
    result = ''
    for row in range(3):
        temp_row = ''
        for col in range(3):
            temp_row += board[row][col] if board[row][col] is not None else ' '
        temp_row += '\n'
        result = temp_row + result

    print(result[:-1])


def make_random_move(board):
    opens = [(i, j) for i in range(3) for j in range(3)
             if board[i][j] is None]

    move = random.choice(opens)
    return move


def minimax(board):
    values = {'X': 1, 'O': -1, True: 0}

    def check(temp_board):
        # Check for a winner
        rows = [row for row in temp_board]
        cols = [[row[i] for row in temp_board] for i in range(3)]
        diagonals = [
            [temp_board[0][0], temp_board[1][1], temp_board[2][2]],
            [temp_board[0][2], temp_board[1][1], temp_board[2][0]]
        ]

        for item1, item2, item3 in rows + cols + diagonals:
            if item1 == item2 == item3 and item1 is not None:
                return item1

        # Check for a tie
        for row in temp_board:
            if None in row:
                return False

        return True

    def get_branches(temp_board, player_turn):
        opens = [(i, j) for i in range(3) for j in range(3)
                 if temp_board[i][j] is None]

        branches = []
        for row, col in opens:
            copied_board = deepcopy(temp_board)
            copied_board[row][col] = 'X' if player_turn else 'O'
            branches.append(copied_board)

        return branches

    def min_move(temp_board):
        complete = check(temp_board)
        if complete:
            return values[complete]

        value = inf
        for branch in get_branches(temp_board, False):
            value = min(value, max_move(branch))

        return value

    def max_move(temp_board):
        complete = check(temp_board)
        if complete:
            return values[complete]

        value = -inf
        for branch in get_branches(temp_board, True):
            value = max(value, min_move(branch))

        return value

    best = -inf
    best_board = None
    for branch in get_branches(board, True):
        value = min_move(branch)
        if value > best:
            best = value
            best_board = branch

    for row in range(3):
        for col in range(3):
            if best_board[row][col] != board[row][col]:
                return row, col


def alpha_beta(board):
    values = {'X': 1, 'O': -1, True: 0}

    def check(temp_board):
        # Check for a winner
        rows = [row for row in temp_board]
        cols = [[row[i] for row in temp_board] for i in range(3)]
        diagonals = [
            [temp_board[0][0], temp_board[1][1], temp_board[2][2]],
            [temp_board[0][2], temp_board[1][1], temp_board[2][0]]
        ]

        for item1, item2, item3 in rows + cols + diagonals:
            if item1 == item2 == item3 and item1 is not None:
                return item1

        # Check for a tie
        for row in temp_board:
            if None in row:
                return False

        return True

    def get_branches(temp_board, player_turn):
        opens = [(i, j) for i in range(3) for j in range(3)
                 if temp_board[i][j] is None]

        branches = []
        for row, col in opens:
            copied_board = deepcopy(temp_board)
            copied_board[row][col] = 'X' if player_turn else 'O'
            branches.append(copied_board)

        return branches

    def min_move(temp_board, alpha, beta):
        complete = check(temp_board)
        if complete:
            return values[complete]

        value = inf
        for branch in get_branches(temp_board, False):
            value = min(value, max_move(branch, alpha, beta))
            if value < alpha:
                return value
            beta = min(beta, value)

        return beta

    def max_move(temp_board, alpha, beta):
        complete = check(temp_board)
        if complete:
            return values[complete]

        value = -inf
        for branch in get_branches(temp_board, True):
            value = max(value, min_move(branch, alpha, beta))
            if value > beta:
                return value
            alpha = max(alpha, value)

        return alpha

    best = -inf
    best_board = None
    alpha = -inf
    beta = inf

    for branch in get_branches(board, True):
        best = max(best, min_move(branch, alpha, beta))
        if best > alpha:
            alpha = best
            best_board = branch

    for row in range(3):
        for col in range(3):
            if best_board[row][col] != board[row][col]:
                return row, col


if __name__ == '__main__':
    #game = Game(player_first=True, auto=minimax)  # might take a while if going first
    game = Game(player_first=False, auto=alpha_beta)  # might take a while if going first
    game.run()
