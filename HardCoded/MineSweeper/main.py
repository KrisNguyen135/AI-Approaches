from minesweeper.msgame import MSGame


W = 10
H = 10
NUM_MINES = 10


if __name__ == '__main__':
    game = MSGame(W, H, NUM_MINES)
    game.print_board()
