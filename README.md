# Artificial Intelligence Approaches in Classic Games
 
Implementing AI ideas and models in the adversarial context of games such as
Nim, Snake, Tic Tac Toe, or even Flappy Birds
 
## Hard-coded logic/algorithms
 
Hard-coded logic, low-level abstraction, no considerable generalization.
 
Games:
- [Nim](https://github.com/KrisNguyen135/AI-Approaches/tree/master/HardCoded/Nim)
- [Minesweeper](https://github.com/KrisNguyen135/AI-Approaches/tree/master/HardCoded/MineSweeper)
(to be mentioned: implementation of a probabilistic approach)
 
## Path-finding algorithms
 
Agents with some degree of autonomy that self-explore the search space, but
there is still significant low-level specification.
 
Games:
- [Maze](https://github.com/KrisNguyen135/AI-Approaches/tree/master/PathFinding/Maze):
breadth-first search (to be mentioned: river crossing puzzles)
- [Sudoku](https://github.com/KrisNguyen135/AI-Approaches/tree/master/PathFinding/Sudoku):
depth-first search
- [Tic Tac Toe](https://github.com/KrisNguyen135/AI-Approaches/tree/master/PathFinding/TicTacToe):
minimax + alpha-beta pruning (to be mentioned: chess)
 
## Genetic algorithm
 
Freedom in generating new solutions, only specifications in the fitness
function and how to preserve good individuals.
 
Games:
- [Optimization of polynomials](https://github.com/KrisNguyen135/AI-Approaches/tree/master/GeneticAlgorithm/Optimization):
a form of search, to be compared with other optimization schemes (e.g., 
gradient descent)
- [Jigsaw](https://github.com/KrisNguyen135/AI-Approaches/tree/master/GeneticAlgorithm/Jigsaw):
customized, more involved fitness crossover functions
 
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
