from HardCoded.MineSweeper.minesweeper import Game  # if executing from directory root
#from minesweeper import Game  # if executing from current directory

import random#; random.seed(1)


class Solver:
    def __init__(self, board):
        self.board = board

    def __str__(self):
        result = ''

        for i in range(15):
            for j in range(15):
                result += str(self.board[j][i]).ljust(4)
            result += '\n'

        return result

    def generate_stats(self):
        """Return a list of coordinates to put flags on or open."""
        to_flag = []
        to_open = []

        for col in range(15):
            for row in range(15):
                temp_cell = self.board[col][row]

                if temp_cell == 'FLAGGED' \
                        or temp_cell == '':
                    continue

                neighbors = Solver.get_cell_neighbors(col, row)

                flagged = []
                unopened = []
                for neighbor in neighbors:
                    cell = self.board[neighbor[0]][neighbor[1]]
                    if cell == 'FLAGGED':
                        flagged.append(neighbor)
                    elif cell == '':
                        unopened.append(neighbor)

                if len(flagged) + len(unopened) == temp_cell:
                    to_flag += unopened

                if len(flagged) == temp_cell:
                    to_open += unopened

        return to_flag, to_open

    @staticmethod
    def get_cell_neighbors(col, row):
        neighbors = []

        if col > 0:
            neighbors.append((col - 1, row))
            if row > 0:
                neighbors.append((col - 1, row - 1))
            if row < 14:
                neighbors.append((col - 1, row + 1))

        if col < 14:
            neighbors.append((col + 1, row))
            if row > 0:
                neighbors.append((col + 1, row - 1))
            if row < 14:
                neighbors.append((col + 1, row + 1))

        if row > 0:
            neighbors.append((col, row - 1))
        if row < 14:
            neighbors.append((col, row + 1))

        return neighbors


def generate_action(board):
    solver = Solver(board)
    to_flag, to_open = solver.generate_stats()

    if len(to_flag) == 0 and len(to_open) == 0:
        unopened = [(col, row) for col in range(15) for row in range(15)
                    if solver.board[col][row] == '']

        if len(unopened) > 0:
            to_open.append(random.choice(unopened))

    return to_flag, to_open


if __name__ == '__main__':
    game = Game(auto=generate_action)
    game.run()
