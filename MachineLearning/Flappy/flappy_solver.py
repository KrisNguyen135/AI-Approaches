from MachineLearning.Flappy.flappy import Game  # if executing from directory root
#from flappy import Game  # if executing from current directory

import neat
import pickle
from MachineLearning.Flappy.visualize import draw_net


def eval_genomes(genomes, config):
    for genome_id, genome in genomes:
        net = neat.nn.FeedForwardNetwork.create(genome, config)
        game = Game(net=net, show=False)
        score = game.run()
        genome.fitness = score


def run(config_file, run_winner=False, winner_name='winner'):
    config = neat.Config(neat.DefaultGenome, neat.DefaultReproduction,
                         neat.DefaultSpeciesSet, neat.DefaultStagnation,
                         config_file)

    # Show the performance of the winner_20_10 net
    if run_winner:
        with open(winner_name, 'rb') as f:
            c = pickle.load(f)

        winner_net = neat.nn.FeedForwardNetwork.create(c, config)
        game = Game(net=winner_net, show=True)
        score = game.run()
        print(f'Score: {score}')

        return

    # Creating initial population and train
    pop = neat.Population(config)

    pop.add_reporter(neat.StdOutReporter(True))
    winner = pop.run(eval_genomes, 300)

    with open(winner_name, 'wb') as f:
        pickle.dump(winner, f)


if __name__ == '__main__':
    #run('config-feedforward')

    #for _ in range(5):
    #    run('config-feedforward', run_winner=True)

    genomes = [
        'winner_20(pop)_10(gen)',
        'winner_50_100',
        'winner_100_100',
        'winner_100_200',
        'winner'
    ]

    config = neat.Config(neat.DefaultGenome, neat.DefaultReproduction,
                         neat.DefaultSpeciesSet, neat.DefaultStagnation,
                         'config-feedforward')

    for g in genomes:
        print(f'Running: {g}')

        with open(g, 'rb') as f:
            c = pickle.load(f)

        dot = draw_net(config, c)
        dot.view()

        run('config-feedforward', run_winner=True, winner_name=g)
