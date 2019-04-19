from GeneticAlgorithm.TravelingSalesman.traveling_salesman import Game
#from traveling_salesman import Game

import random


class Solver:
    def __init__(self, n_cities, dis_matrix, viz_func,
                 pop_size=100, random_size=0.2, elite_size=0.1, n_gens=10):

        self.n_cities = n_cities
        self.dis_matrix = dis_matrix
        self.cities = list(range(self.n_cities))

        self.viz_func = viz_func

        self.pop_size = pop_size
        self.random_size = random_size
        self.elite_size = elite_size
        self.n_gens = n_gens

        self.prev_pop = None
        self.temp_pop = []

    def fitness(self, ind):
        return sum(
            self.dis_matrix[ind[i]][ind[i + 1]] for i in range(len(ind) - 1))

    def crossover(self, parent1, parent2):
        # Pick out a random part of `parent1` and project it to child.
        # The part is approximately around half as long as the length of a parent.
        start_index = random.randint(0, self.n_cities - 1)
        end_index = (start_index + self.n_cities // 2) % self.n_cities
        start_index, end_index = min(start_index, end_index), max(start_index, end_index)

        child = [None for _ in range(self.n_cities + 1)]
        for i in range(start_index, end_index):
            child[i] = parent1[i]

        # Project the missing cities from `parent2` to child
        remain_cities = [city for city in parent2[:-1] if city not in child]
        for i in range(len(child) - 1):
            if child[i] is None:
                child[i] = remain_cities.pop(0)

        # Make sure the endpoints are the same
        child[-1] = child[0]

        return child

    def generate_random_pop(self, pop_size=100):
        pop = []
        for i in range(pop_size):
            ind = random.sample(self.cities, k=self.n_cities)
            ind.append(ind[0])
            pop.append(ind)

        return pop

    def generate_new_pop(self):
        fitnesses = [self.fitness(ind) for ind in self.temp_pop]
        sorted_pop = [ind for fitness, ind in
                      reversed(sorted(zip(fitnesses, self.temp_pop)))]

        id_cdf = [i for i in range(len(sorted_pop)) for _ in range(i)]

        # Elitism
        if self.prev_pop is not None:
            new_pop = self.prev_pop[: -int(self.pop_size * self.elite_size)]
        else:
            new_pop = []

        # Generate via crossover
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
        self.temp_pop = self.generate_random_pop(self.pop_size)

        for i in range(self.n_gens):
            self.temp_pop, self.prev_pop = self.generate_new_pop()
            print(f'Current best individual of {i}-th generation:')
            print(self.prev_pop[-1])
            self.viz_func(self.prev_pop[-1])
            print(f'Fitness: {self.fitness(self.prev_pop[-1])}')

        return self.prev_pop[-1]


if __name__ == '__main__':
    game = Game(7)
    solver = Solver(7, game.dis_matrix, game.visualize_solution, n_gens=5)
    solver.run()
