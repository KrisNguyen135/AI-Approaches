from ReinforcementLearning.Snake.snake import Game
# from snake import Game

import os
import numpy as np
import random


class SparseSolver:
    file = 'output/sparse.csv'

    def __init__(self):
        if os.path.isfile(SparseSolver.file):
            self.q_table = np.genfromtxt(
                SparseSolver.file,
                delimiter=','
            )
        else:
            self.q_table = np.zeros((38, 38, 4, 4), dtype=int)  # each delta // 10

        self.training = False

    def make_move(self, delta_x, delta_y, direction):
        move = np.argmax(self.q_table[delta_x, delta_y, direction])
        if self.training:
            self.temp_sequence.append((delta_x, delta_y, direction, move))

        return move

    def train(self, num_rounds):
        print('Started training...')

        self.training = True
        for round in range(num_rounds):
            print()
            print('=' * 40)
            print(f'Round {round}:')

            self.temp_sequence = []

            game = Game(show=False, auto=self.make_move)


if __name__ == '__main__':
    game = Game(show=True)
    game.run()
