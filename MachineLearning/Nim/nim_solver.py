from MachineLearning.Nim.nim import Game  # if executing from directory root
#from nim import Game  # if executing from current directory

import os
from sklearn import svm
import joblib
import random
import numpy as np
import matplotlib.pyplot as plt


class Solver:
    def __init__(self, max_sticks):
        self.max_sticks = max_sticks
        self.filename = 'model.joblib'

        if os.path.isfile(self.filename):
            self.model = joblib.load(self.filename)
        else:
            self.model = svm.SVC()

        self.training = False

    def make_move(self, remain_sticks):
        if self.training:
            move = random.randint(1, min(self.max_sticks, remain_sticks))
            self.temp_X.append([remain_sticks, move])

            return move

        predictions = self.model.predict([
            [remain_sticks, move]
            for move in range(1, min(self.max_sticks, remain_sticks) + 1)
        ])

        potential_wins = (np.argwhere(predictions == 1) + 1).flatten()
        if len(potential_wins) == 0:
            return random.randint(1, min(self.max_sticks, remain_sticks))

        return random.choice(potential_wins)

    def train(self, num_samples, num_stick_choices, visualize=False):
        self.training = True

        X = []
        y = []

        # Generate the training data.
        num_wins = 0
        num_losses = 0

        while num_wins < num_samples or num_losses < num_samples:
            self.temp_X = []

            game = Game(
                random.choice(num_stick_choices),
                self.max_sticks,
                player_first=(random.randint(0, 1) == 0),
                hard=True,
                auto=self.make_move,
                silent=True
            )
            result = game.run()
            temp_y = [result for _ in range(len(self.temp_X))]

            if num_wins < num_samples and result == 1:
                X += self.temp_X
                y += temp_y
                num_wins += 1

            if num_losses < num_samples and result == -1:
                X += self.temp_X
                y += temp_y
                num_losses += 1

        # Train the model.
        self.model.fit(X, y)

        # Visualize the maximum margin.
        X = np.array(X)
        if visualize:
            plt.scatter(X[:, 0], X[:, 1], c=y, s=50, cmap='autumn')

            ax = plt.gca()
            xlim = ax.get_xlim()
            ylim = ax.get_ylim()

            # Plot the grid.
            x = np.linspace(xlim[0], xlim[1], 30)
            y = np.linspace(ylim[0], ylim[1], 30)
            Y, X = np.meshgrid(y, x)
            xy = np.vstack([X.ravel(), Y.ravel()]).T
            P = self.model.decision_function(xy).reshape(X.shape)

            # Plot the decision boundary and margins
            ax.contour(X, Y, P, colors='k', levels=[-1, 0, 1], alpha=0.5,
                       linestyles=['--', '-', '--'])

            # Plot the support vectors.
            ax.scatter(self.model.support_vectors_[:, 0],
                       self.model.support_vectors_[:, 1],
                       s=300, linewidth=1, facecolors='none')
            ax.set_xlim(xlim)
            ax.set_ylim(ylim)

            plt.show()

    def save(self):
        joblib.dump(self.model, self.filename)


if __name__ == '__main__':
    stick_choices = list(range(5, 20))

    solver = Solver(3)
    #solver.train(10000, stick_choices, visualize=True)
    #solver.save()

    '''num_wins = 0
    for _ in range(10):
        game = Game(random.choice(stick_choices), 3, auto=solver.make_move,
                    silent=True)
        result = game.run()
        if result == 1:
            num_wins += 1

    print(f'Number of wins: {num_wins} / 10')'''
