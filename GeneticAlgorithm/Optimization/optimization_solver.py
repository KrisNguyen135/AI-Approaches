from GeneticAlgorithm.Optimization.optimization import Game  # if executing from directory root
# from optimization import Game  # if executing from current directory

import random


class Solver:
    def __init__(self, length, game, pop_size=100, random_size=0.2,
                 mutation_prop=0.01, n_gens=10):
        self.length = length
        self.game = game

        self.pop_size = pop_size
        self.random_size = random_size
        self.mutation_prop = mutation_prop
        self.n_gens = n_gens

        self.prev_pop = None
        self.temp_pop = []

    def fitness(self, ind):
        return self.game.get_value(int(ind, 2))

    def crossover(self, parent1, parent2):
        child = parent1[: self.length // 2] + parent2[self.length // 2:]
        if random.uniform(0, 1) < self.mutation_prop:
            mutation_index = random.choice(range(self.length))
            child = child[: mutation_index] \
                    + str((int(child[mutation_index]) + 1) % 2) \
                    + child[mutation_index + 1:]

        return child

    def generate_random_pop(self, pop_size):
        pop = []
        for i in range(pop_size):
            temp_ind = ''
            for _ in range(self.length):
                temp_ind += str(random.randint(0, 1))
            pop.append(temp_ind)

        return pop

    def generate_new_pop(self):
        fitnesses = [self.fitness(ind) for ind in self.temp_pop]
        sorted_pop = [ind for fitness, ind in
                      reversed(sorted(zip(fitnesses, self.temp_pop)))]

        # Simple CDF of indices for individuals in the population.
        # Individuals with better fitness have their indices repeated more.
        id_cdf = [i for i in range(len(sorted_pop)) for _ in range(i)]

        new_pop = []
        for i in range(int(self.pop_size * (1 - self.random_size))):
            parent1_id = 0
            parent2_id = 0

            while parent1_id == parent2_id:
                parent1_id, parent2_id = random.sample(id_cdf, 2)

            parent1 = sorted_pop[parent1_id]
            parent2 = sorted_pop[parent2_id]
            child = self.crossover(parent1, parent2)

            new_pop.append(child)

        new_pop += self.generate_random_pop(self.pop_size - len(new_pop))

        return new_pop, sorted_pop

    def run(self):
        # Create initial population
        self.temp_pop = self.generate_random_pop(self.pop_size)

        # Run evolution
        for i in range(self.n_gens):
            self.temp_pop, self.prev_pop = self.generate_new_pop()
            print(f'Current best individual of {i}-th generation:')
            print(self.prev_pop[-1])
            print(f'Fitness: {self.fitness(self.prev_pop[-1])}')

        return self.prev_pop[-1]


if __name__ == '__main__':
    game = Game(3, (0, 1024), [1, -205, 100, -1000])
    #solver = Solver(10, game, pop_size=100, n_gens=10)
    #solver = Solver(10, game, pop_size=200, n_gens=20)
    solver = Solver(10, game, pop_size=400, n_gens=40)
    solver.run()
