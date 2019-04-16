from HardCoded.Nim.nim import Game  # if executing from directory root
#from nim import Game  # if executing from current directory

import os
import pandas as pd


class Solver:
    def __init__(self, num_sticks, max_sticks, output=None):
        self.num_sticks = num_sticks
        self.max_sticks = max_sticks

        if output is None:
            self.output = f'output/{max_sticks}.csv'
        else:
            self.output = output

        if os.path.isfile(self.output):
            self.q_table = pd.read_csv(self.output, index_col=0)
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
                data = [[0 for _ in range(max_sticks)] for __ in range(num_sticks)],
                index = list(range(1, num_sticks + 1)),
                columns = [str(i) for i in range(1, max_sticks + 1)]
            )

        print(self.q_table)


if __name__ == '__main__':
    #game = Game()
    #game.run()

    solver = Solver(13, 3, output='output/3.csv')
