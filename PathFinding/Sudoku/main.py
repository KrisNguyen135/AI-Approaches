from PathFinding.Sudoku.sudoku import Game  # if executing from directory root
#from sudoku import Game  # if executing from current directory


if __name__ == '__main__':
    game = Game(input_='input/hard.txt')
    print(game)
