import matplotlib.pyplot as plt


class Game:
    def __init__(self, input_='input/small.txt', auto=None):
        self.input_ = input_
        with open(self.input_, 'r') as f:
            lines = f.readlines()

        # read in input from text file
        self.height, self.width = map(int, lines[0].split(' '))
        self.start_pos = int(lines[1])
        self.board = []
        for n_row in range(self.height):
            self.board.append(list(lines[n_row + 2][:-1]))

        # encode text data
        self.board = [
            [1 if self.board[i][j] == '#' else 0 for j in range(self.width)]
            for i in range(self.height)
        ]

        self.auto = auto

    def run(self):
        if self.auto is not None:
            for path in self.auto(
                    self.board, (self.start_pos, 0), self.width - 1):

                plt.matshow(self.board)
                plt.xticks([])
                plt.yticks([])

                for i in range(len(path) - 1):
                    start = path[i]
                    end = path[i + 1]
                    plt.plot([start[1], end[1]], [start[0], end[0]], 'r')

                plt.pause(0.05)
                plt.close()

                if end[1] == self.width - 1:
                    self.in_progress = False
