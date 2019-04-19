from GeneticAlgorithm.TravelingSalesman.traveling_salesman import Game
#from traveling_salesman import Game

if __name__ == '__main__':
    game = Game(4)
    print(game.dis_matrix)
    print(game.visualize_solution([0, 1, 2, 3, 0]))
