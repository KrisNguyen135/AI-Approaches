from MachineLearning.Nim.nim import Game  # if executing from directory root
#from nim import Game  # if executing from current directory


if __name__ == '__main__':
    game = Game(player_first=False)
    game.run()
