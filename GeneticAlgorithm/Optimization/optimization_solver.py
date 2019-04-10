from GeneticAlgorithm.Optimization.optimization import Game  # if executing from directory root
#from optimization import Game  # if executing from current directory


class Solver:
    def __init__(self, x_log_limits, game, pop_size=100, n_gens=10):
        self.x_log_limits = x_log_limits
        self.game = game

        self.pop_size = pop_size
        self.n_gens = n_gens

        self.prev_pop = None
        self.temp_pop = []

    def fitness(self, ind):
        return self.game.get_value(int(ind, 2))

    def select(self):
        return

    def crossover(self):
        return

    def run(self):
        return


if __name__ == '__main__':
    game = Game(2, (-10, 10), [1, -2, 1])
