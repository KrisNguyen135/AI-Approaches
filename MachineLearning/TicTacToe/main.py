from MachineLearning.TicTacToe.tictactoe import Game  # if executing from directory root
#from tictactoe import Game  # if executing from current directory


if __name__ == '__main__':
    game = Game(player_first=True)
    game.run()
