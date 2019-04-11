from GeneticAlgorithm.Jigsaw.jigsaw import Game  # if executing from directory root
#from jigsaw import Game  # if executing from current directory


if __name__ == '__main__':
    game = Game('input/michelangelo-creation-of-adam.jpg')
    pieces = game.pieces
    print(pieces)
    print(pieces.shape)
