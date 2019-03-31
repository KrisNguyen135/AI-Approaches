from PathFinding.Maze.maze import Game  # if executing from directory root
#from maze import Game  # if executing from current directory


if __name__ == '__main__':
    game = Game(input_='input/large.txt')
    game.run()
