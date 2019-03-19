from flappy import Game


if __name__ == '__main__':
    for _ in range(3):
        game = Game(show=False)
        score = game.run()
        print(score)
