from HardCoded.Nim.nim import Game  # if executing from directory root
#from nim import Game  # if executing from current directory

import random


def make_move(num_sticks, max_sticks):
    if num_sticks <= max_sticks:
        return num_sticks
    else:
        remainder = num_sticks % (max_sticks + 1)
        if remainder == 0:
            return random.randint(1, max_sticks)
        else:
            return remainder


if __name__ == '__main__':
    game = Game(auto=make_move)
    game.run()
