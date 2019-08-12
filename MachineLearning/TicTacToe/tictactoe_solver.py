from MachineLearning.TicTacToe.tictactoe import Game  # if executing from directory root
#from tictactoe import Game  # if executing from current directory

import torch


class TicTacToeNet(torch.nn.Module):
    def __init__(self):
        super(TicTacToeNet, self).__init__()
        self.fc1 = torch.nn.Linear(9, 32)
        self.fc2 = torch.nn.Linear(32, 64)
        self.output = torch.nn.Linear(64, 9)

    def forward(self, board):
        x = TicTacToeNet.convert_board(board)

        out = self.fc1(x)
        out = self.fc2(out)
        out = self.output(out)

        return out

    @staticmethod
    def convert_board(board):
        values = {'X': 1, 'O': -1, None: 0}

        return [values[board[row][col]]
                for col in range(3) for row in range(3)]
