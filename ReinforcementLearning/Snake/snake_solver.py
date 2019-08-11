from ReinforcementLearning.Snake.snake import Game
# from snake import Game

import os
import numpy as np; np.random.seed(0)
from tqdm import tqdm


class SparseSolver:
    def __init__(self, filename='output/sparse.npy'):
        self.filename = filename
        if os.path.isfile(filename):
            self.q_table = np.load(filename)
        else:
            self.q_table = np.zeros((3, 3, 4, 4), dtype=int)

        self.training = False

    def make_move(self, delta_x, delta_y, direction):
        def convert_delta(delta):
            if delta < 0:
                return 0

            if delta == 0:
                return 1

            return 2

        delta_x = convert_delta(delta_x)
        delta_y = convert_delta(delta_y)

        max_score = np.amax(self.q_table[delta_x, delta_y, direction])
        move = np.random.choice(np.argwhere(
            self.q_table[delta_x, delta_y, direction] == max_score).flatten())
        if self.training:
            self.temp_sequence.append((delta_x, delta_y, direction, move))

        return move

    def train(self, num_rounds):
        self.training = True

        for _ in tqdm(range(num_rounds), desc='Training progress'):
            self.temp_sequence = []

            game = Game(show=False, auto=self.make_move)
            result = game.run()
            for item in self.temp_sequence:
                delta_x, delta_y, direction, move = item
                self.q_table[delta_x, delta_y, direction, move] += result

    def save(self):
        np.save(self.filename, self.q_table)


class AuxReward:
    def __init__(self, filename='output/aux.npy'):
        self.filename = filename
        if os.path.isfile(filename):
            self.q_table = np.load(filename)
        else:
            self.q_table = np.zeros((3, 3, 4, 4), dtype=float)

        self.training = False

    @staticmethod
    def convert_delta(delta):
        if delta < 0:
            return 0

        if delta == 0:
            return 1

        return 2

    def make_move(self, delta_x, delta_y, direction):
        norm_delta_x = AuxReward.convert_delta(delta_x)
        norm_delta_y = AuxReward.convert_delta(delta_y)

        max_score = np.amax(self.q_table[norm_delta_x, norm_delta_y, direction])
        move = np.random.choice(np.argwhere(
            self.q_table[norm_delta_x, norm_delta_y, direction] == max_score
        ).flatten())
        if self.training:
            self.temp_sequence.append((delta_x, delta_y, direction, move))

        return move

    def train(self, num_rounds):
        self.training = True

        for _ in tqdm(range(num_rounds), desc='Training progress'):
            self.temp_sequence = []

            game = Game(show=False, auto=self.make_move)
            _ = game.run()  # no need to get the final result
            num_steps = len(self.temp_sequence)

            for i in range(num_steps - 1):
                delta_x, delta_y, direction, move = self.temp_sequence[i]
                next_delta_x, next_delta_y, _, _ = self.temp_sequence[i + 1]

                norm_delta_x = AuxReward.convert_delta(delta_x)
                norm_delta_y = AuxReward.convert_delta(delta_y)

                # Check for success in eating.
                if abs(delta_x - next_delta_x) > 10 \
                        or abs(delta_y - next_delta_y) > 10:
                    self.q_table[norm_delta_x, norm_delta_y, direction, move] += \
                        10 / num_steps

                # Check for a decrease in the distance to the food.
                elif abs(delta_x) >= abs(next_delta_x) \
                        and abs(delta_y) >= abs(next_delta_y):
                    self.q_table[norm_delta_x, norm_delta_y, direction, move] += \
                        1 / num_steps

                elif abs(delta_x) < abs(next_delta_x) \
                        or abs(delta_y) < abs(next_delta_y):
                    self.q_table[norm_delta_x, norm_delta_y, direction, move] -= \
                        1 / num_steps

    def save(self):
        np.save(self.filename, self.q_table)


if __name__ == '__main__':
    # Implement a sparse solver.
    '''solver = SparseSolver()
    solver.train(10000)

    for _ in range(5):
        game = Game(auto=solver.make_move, show=True)
        game.run()

    solver.save()'''

    # Implement a solver with an auxiliary reward function.
    solver = AuxReward()
    solver.train(10000)

    for _ in range(5):
        game = Game(auto=solver.make_move, show=True)
        game.run()

    print(solver.q_table)
