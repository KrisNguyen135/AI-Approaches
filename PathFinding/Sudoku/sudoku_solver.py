from PathFinding.Sudoku.sudoku import Game  # if executing from directory root
#from sudoku import Game  # if executing from current directory

from copy import deepcopy


class Solver:
    def __init__(self, board):
        self.board = board

    def get_presence(self):
        present_in_row = []
        present_in_col = []
        present_in_block = []

        # Initialize presences
        for i in range(9):
            present_in_row.append({})
            present_in_col.append({})
            present_in_block.append({})
            for num in range(1, 10):
                present_in_row[i][num] = False
                present_in_col[i][num] = False
                present_in_block[i][num] = False

        # Compute presences
        for row in range(9):
            for col in range(9):
                temp_cell = self.board[row][col]
                if temp_cell != 0:
                    present_in_row[row][temp_cell] = True
                    present_in_col[col][temp_cell] = True
                    present_in_block[row//3 * 3 + col//3][temp_cell] = True

        return present_in_row, present_in_col, present_in_block

    def get_possible_values(self):
        possible_values = {}

        present_in_row, present_in_col, present_in_block = self.get_presence()

        for row in range(9):
            for col in range(9):
                if self.board[row][col] == 0:
                    possible_values[(row, col)] = []

                    for num in range(1, 10):
                        if present_in_row[row][num] \
                                or present_in_col[col][num] \
                                or present_in_block[row//3 * 3 + col//3][num]:
                            continue  # continue if number is already present

                        possible_values[(row, col)].append(num)

        return possible_values

    def auto_update(self):
        update_again = False
        possible_values = self.get_possible_values()

        for (row, col), values in possible_values.items():
            if len(values) == 1:
                update_again = True
                self.board[row][col] = values[0]

        if update_again:
            self.auto_update()

    def recur_solve(self):
        self.auto_update()

        possible_values = self.get_possible_values()
        if len(possible_values) == 0:
            return True

        branch_location = None
        min_n_values = 10
        for location, value in possible_values.items():
            if len(value) == 0:
                return False
            if len(value) < min_n_values:
                min_n_values = len(value)
                branch_location = location

        for branch_value in possible_values[branch_location]:
            # To discuss: number of branches needed as difficulty increases
            saved_board = deepcopy(self.board)
            self.board[branch_location[0]][branch_location[1]] = branch_value
            valid_solution = self.recur_solve()

            if not valid_solution:
                self.board = saved_board
            else:
                return True

        return False

    def solve(self):
        self.recur_solve()


if __name__ == '__main__':
    game = Game(input_='input/hard.txt')
    print(game)

    solver = Solver(game.board)
    solver.solve()
    for row in range(9):
        for col in range(9):
            game.update(row, col, solver.board[row][col])

    print(game)
