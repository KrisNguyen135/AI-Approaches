import random


class Game:
    """Command line game of Nim."""

    def __init__(self, num_sticks=13, max_sticks=3, player_first=True,
                 hard=False, auto=None, silent=False):

        self.player_first = player_first
        self.hard= hard
        self.auto = auto

        self.num_sticks = num_sticks
        self.max_sticks = max_sticks
        self.valids = [i for i in range(1, self.max_sticks + 1)]

        self.silent = silent

    def ask_for_move(self):
        while True:
            if self.auto is not None:
                move = self.auto(self.num_sticks)
            else:
                move = input('Enter the number of sticks to take: ')

            try:
                move = int(move)
                if move in self.valids and move <= self.num_sticks:
                    return move
            except ValueError:
                pass

            print(move in self.valids, move <= self.num_sticks)
            print('Invalid input.')

    def run(self):
        if not self.silent:
            print(f'Total number of sticks: {self.num_sticks}')
            print(f'Maximum number of sticks to take each turn: {self.max_sticks}')

        if self.player_first:
            turn = 0
        else:
            turn = 1

        while self.num_sticks:
            if not self.silent:
                print()
                print(f'Number of sticks remaining: {self.num_sticks}')
                print('| ' * self.num_sticks)

            if turn == 0:
                if not self.silent:
                    print("Player's turn")

                move = self.ask_for_move()

            else:
                if not self.silent:
                    print("Computer's turn")

                if self.hard:
                    move = self.num_sticks % (self.max_sticks + 1)
                    if move == 0:
                        move = random.randint(1, self.max_sticks)
                else:
                    move = random.randint(
                        1, min(self.max_sticks, self.num_sticks))

            if not self.silent:
                print(f'{move} stick(s) taken')
            self.num_sticks -= move

            turn = (turn + 1) % 2

        if not self.silent:
            print('No sticks remaining')
        if turn == 0:
            if not self.silent:
                print('Computer won')
            return -1
        else:
            if not self.silent:
                print('Player won')
            return 1
