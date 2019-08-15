from CombinedDeepLearning.Flappy.flappy import Game  # if executing from directory root
#from flappy import Game  # if executing from current directory


if __name__ == '__main__':
    for _ in range(3):
        game = Game(show=False)
        score = game.run()
        print(score)
