from ReinforcementLearning.Snake.snake import Game
# from snake import Game

import os
import numpy as np
import random


class SparseSolver:
    file = 'output/sparse.npy'

    def __init__(self, desired_length=10):
        if os.path.isfile(SparseSolver.file):
            self.q_table = np.load(SparseSolver.file)
        else:
            self.q_table = np.zeros((84, 84, 4, 4), dtype=int)  # each side // 10

        self.desired_length = desired_length
        self.training = False

    def make_move(self, delta_x, delta_y, direction):
        # Normalize the deltas.
        delta_x = (delta_x + 420) // 10
        delta_y = (delta_y + 420) // 10

        #print(delta_x, delta_y)
        move = np.argmax(self.q_table[delta_x, delta_y, direction])
        if self.training:
            self.temp_sequence.append((delta_x, delta_y, direction, move))

        return move

    def train(self, num_rounds):
        print('Started training...')

        self.training = True
        for round in range(num_rounds):
            if round % 1000 == 0:
                print()
                print('=' * 40)
                print(f'Round {round}')

            self.temp_sequence = []

            game = Game(show=False, auto=self.make_move)
            result = game.run()
            for item in self.temp_sequence:
                delta_x, delta_y, direction, move = item
                self.q_table[delta_x, delta_y, direction, move] += \
                    result - self.desired_length

        print('Finished training')

    def save(self):
        np.save(SparseSolver.file, self.q_table)


if __name__ == '__main__':
    # Implementation of a spare solver.
    '''solver = SparseSolver(desired_length=5)
    solver.train(100000)

    game = Game(auto=solver.make_move, show=True)
    game.run()

    for index, item in np.ndenumerate(solver.q_table):
        if item != 0:
            print(index, item)

    solver.save()'''
