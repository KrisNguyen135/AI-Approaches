from GeneticAlgorithm.Jigsaw.jigsaw import Game  # if executing from directory root
#from jigsaw import Game  # if executing from current directory

import numpy as np


class Solver:
    def __init__(self, pieces):
        self.threshold = self.generate_threshold(pieces, p=93)

        self.piece_edges = np.array([np.array([
            piece[0, :],
            piece[:, -1],
            piece[-1, :],
            piece[:, 0]
        ]) for piece in pieces])

    def generate_threshold(self, pieces, p=100):
        differences = []

        for piece in pieces:
            differences.append(np.sum((piece[0, :] - piece[1, :]) ** 2))
            differences.append(np.sum((piece[:, -1] - piece[:, -2]) ** 2))
            differences.append(np.sum((piece[-1, :] - piece[-2, :]) ** 2))
            differences.append(np.sum((piece[:, 0] - piece[:, 1]) ** 2))

        return np.percentile(differences, p)


if __name__ == '__main__':
    game = Game('input/michelangelo-creation-of-adam.jpg')
    pieces = game.pieces
    print(pieces)
    print(pieces.shape)
