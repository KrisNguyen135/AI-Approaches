# Artificial Intelligence Approaches in Classic Games
 Implementing AI ideas and models in the adversarial context of games such as
 Nim, Snake, or even Flappy Birds
 
 ## Hard-coded logic/algorithms
 
 Hard-coded logic, low-level abstraction, not a lot of generalization.
 
 Games:
 - [Nim](https://github.com/KrisNguyen135/AI-Approaches/tree/master/HardCoded/Nim)
 - [Minesweeper](https://github.com/KrisNguyen135/AI-Approaches/tree/master/HardCoded/MineSweeper)
 (future adjustment: implementing a probabilistic approach)
 
 ## Path-finding algorithms
 
 Agents with some degree of autonomy that self-explore the search space, but
 there is still a lot of low-level specification.
 
 Algorithms:
 - Depth-first, breadth-first, best-first
 - Minimax + Alpha-Beta pruning
 - Dijkstra
 - A and A*
 
 Games:
 - Sudoku
 - Tic Tac Toe
 - Maze
 - To mention: River-crossing, Chess
 
 ## Genetic algorithm
 
 Freedom in generating new solutions, only specifications in the fitness
 function and how to preserve good individuals.
 
 Games:
 - Optimization of polynomials
 - Jigsaw
 
 ## Reinforcement learning
 
 Self-exploring agents, only specifications in the scoring function, including
 Q-learning.
 
 Games: 
 - Nim (revisited)
 - Snake
 
 ## Machine learning & Deep learning
 
 Higher level of abstraction, relies on recognizing the pattern as opposed to
 random exploration or low-level specification. 
 
 Games:
 - Nim (revisited): line fitting with ML
 - Minesweeper (revisited): pattern processing with DL
 
 ## NEAT
 
 Combine deep learning and genetic algorithm.
 
 Games:
 - [Flappy Birds](https://github.com/KrisNguyen135/AI-Approaches/tree/master/NEAT/Flappy)
 - Pacman
 - Chrome T-Rex
 
 ## Deep reinforcement learning
 
 Combine deep learning and reinforcement learning.
 
 Games: **Pending**
 