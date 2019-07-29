from ReinforcementLearning.Nim.nim import Game  # if executing from directory root
#from nim import Game  # if executing from current directory

import os
import pandas as pd
import random


class Solver:
    def __init__(self, num_sticks, max_sticks):
        self.num_sticks = num_sticks
        self.max_sticks = max_sticks
        self.file = f'output/{max_sticks}.csv'

        if os.path.isfile(self.file):
            self.q_table = pd.read_csv(self.file, index_col=0)
            if self.q_table.shape[0] < num_sticks:
                self.q_table = pd.concat([
                    self.q_table,
                    pd.DataFrame(
                        data=[
                            [0 for __ in range(max_sticks)]
                            for _ in range(num_sticks - self.q_table.shape[0])
                        ],
                        index=list(range(self.q_table.shape[0] + 1, num_sticks + 1)),
                        columns=[str(i) for i in range(1, max_sticks + 1)]
                    )
                ])
        else:
            self.q_table = pd.DataFrame(
                data=[[0 for _ in range(max_sticks)] for __ in range(num_sticks)],
                index=list(range(1, num_sticks + 1)),
                columns=[str(i) for i in range(1, max_sticks + 1)]
            )

            for row in range(1, max_sticks + 1):
                for col in range(1, max_sticks + 1):
                    if row != col:
                        self.q_table.loc[row, str(col)] = -1
                    else:
                        self.q_table.loc[row, str(col)] = 1

        self.training = False

    def make_move(self, remain_sticks):
        move = self.q_table.idxmax(axis=1).loc[remain_sticks]
        if self.training:
            self.temp_sequence.append((remain_sticks, move))

        return move

    def train(self, num_rounds):
        print('Started training...')

        self.training = True
        for round in range(num_rounds):
            print()
            print('=' * 40)
            print(f'Round {round}')

            self.temp_sequence = []

            game = Game(
                self.num_sticks,
                self.max_sticks,
                player_first=(random.randint(0, 1) == 0),
                hard=True,
                auto=self.make_move
            )
            result = game.run()
            for row, col in self.temp_sequence:
                self.q_table.loc[row, str(col)] += result

        print('Finished training')

    def save(self):
        self.q_table.to_csv(self.file)


if __name__ == '__main__':
    '''solver = Solver(13, 3')
    solver.train(1000)

    #game = Game(13, 3, auto=solver.make_move)
    #game.run()

    solver.save()'''

    solver = Solver(10, 3)
    game = Game(13, 3, auto=solver.make_move)
    game.run()
