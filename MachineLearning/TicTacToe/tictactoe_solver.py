from MachineLearning.TicTacToe.tictactoe import Game  # if executing from directory root
#from tictactoe import Game  # if executing from current directory

import os
import torch; torch.manual_seed(0)
import random; random.seed(0)
import numpy as np
from tqdm import tqdm


class TicTacToeNet(torch.nn.Module):
    def __init__(self):
        super(TicTacToeNet, self).__init__()
        self.fc1 = torch.nn.Linear(9, 32)
        self.fc2 = torch.nn.Linear(32, 64)
        self.relu = torch.nn.ReLU()
        self.output = torch.nn.Linear(64, 9)

    def forward(self, x):
        out = self.fc1(x)
        out = self.relu(out)
        out = self.fc2(out)
        out = self.relu(out)
        out = self.output(out)

        return out


class Solver:
    def __init__(self):
        self.model = TicTacToeNet()
        self.filename = 'model.pth'

        if os.path.isfile(self.filename):
            self.model.load_state_dict(torch.load(self.filename))

        self.training = False

    def make_move(self, board):
        if self.training:
            opens = [(i, j) for i in range(3) for j in range(3)
                     if board[i][j] is None]
            move = random.choice(opens)
            self.temp_X.append(Solver.convert_board(board))
            self.temp_y.append(move[0] * 3 + move[1])

            return move

        with torch.no_grad():
            '''output = self.model(
                torch.tensor(board, dtype=torch.float, requires_grad=True)
            ).view(1, -1)'''

            #out = self.model(Solver.convert_board(board)).numpy()
            out = self.model(
                torch.tensor(Solver.convert_board(board), dtype=torch.float)
            ).numpy()
            pred = np.argmax(out)

            return pred // 3, pred % 3

    def train(self, num_samples):
        self.training = True

        X = []
        y = []

        # Generate the training data.
        running_samples = 0
        gen_progress = tqdm(total=num_samples, desc='Data generation progress')

        while running_samples < num_samples:
            self.temp_X = []
            self.temp_y = []

            game = Game(
                player_first=(random.randint(0, 1) == 0),
                auto=self.make_move,
                show=False
            )
            result = game.run()
            if result is not None and result > 0:
                X += self.temp_X
                y += self.temp_y

                running_samples += len(self.temp_y)
                gen_progress.update(len(self.temp_y))

        gen_progress.close()

        #print(X)
        #print(y)

        # Train the model.
        num_epochs = 30
        learning_rate = 0.001

        criterion = torch.nn.CrossEntropyLoss()
        optimizer = torch.optim.Adam(self.model.parameters(), lr=learning_rate)

        for _ in tqdm(range(num_epochs), desc='Training progress'):
            for board, move in zip(X, y):
                output = self.model(
                    torch.tensor(board, dtype=torch.float, requires_grad=True)
                ).view(1, -1)
                target = torch.tensor(move, dtype=torch.long).view(-1)

                loss = criterion(output, target)

                optimizer.zero_grad()
                loss.backward()
                optimizer.step()

    def save(self):
        torch.save(self.model.state_dict(), self.filename)

    @staticmethod
    def convert_board(board):
        values = {'X': 1, 'O': -1, None: 0}

        return [values[board[row][col]]
                for col in range(3) for row in range(3)]


if __name__ == '__main__':
    solver = Solver()
    #solver.train(1000)
    #solver.save()

    '''for param_tensor in solver.model.state_dict():
        print(param_tensor)
        print(solver.model.state_dict()[param_tensor])
        print()'''

    num_wins = 0
    for _ in range(10):
        game = Game(player_first=(random.randint(0, 1) == 0),
                    auto=solver.make_move)
        result = game.run()
        if result == 1:
            num_wins += 1

    print(f'Number of wins: {num_wins} / 10')
