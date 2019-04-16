import random


class Game:
    """Command line game of Nim."""

    def __init__(self, num_sticks=13, max_sticks=3,
                 player_first=True, auto=None):

        self.player_first = player_first
        self.auto = auto

        self.num_sticks = num_sticks
        self.max_sticks = max_sticks
        self.valids = [i for i in range(1, self.max_sticks + 1)]

    def ask_for_move(self):
        while True:
            if self.auto is not None:
                move = self.auto(self.num_sticks, self.max_sticks)
            else:
                move = input('Enter the number of sticks to take: ')

            try:
                move = int(move)
                if move in self.valids and move <= self.num_sticks:
                    return move
            except ValueError:
                pass

            print('Invalid input.')

    def run(self):
        print(f'Total number of sticks: {self.num_sticks}')
        print(f'Maximum number of sticks to take each turn: {self.max_sticks}')

        if self.player_first:
            turn = 0
        else:
            turn = 1

        while self.num_sticks:
            print()
            print(f'Number of sticks remaining: {self.num_sticks}')
            print('| ' * self.num_sticks)

            if turn == 0:
                print("Player's turn")
                move = self.ask_for_move()
            else:
                print("Computer's turn")
                move = random.randint(1, min(self.max_sticks, self.num_sticks))

            print(f'{move} stick(s) taken')
            self.num_sticks -= move

            turn = (turn + 1) % 2

        print('No sticks remaining')
        if turn == 0:
            print('Computer won')
        else:
            print('Player won')
