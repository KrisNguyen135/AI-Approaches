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
breadth-first search (to be mentioned: depth-first search, river crossing puzzles)
- [Sudoku](https://github.com/KrisNguyen135/AI-Approaches/tree/master/PathFinding/Sudoku):
depth-first search (to be mentioned: why not BFS)
```
Before:
+-------+-------+-------+
| 3 0 0 | 2 0 0 | 0 0 0 |
| 0 0 0 | 1 0 7 | 0 0 0 |
| 7 0 6 | 0 3 0 | 5 0 0 |
+-------+-------+-------+
| 0 7 0 | 0 0 9 | 0 8 0 |
| 9 0 0 | 0 2 0 | 0 0 4 |
| 0 1 0 | 8 0 0 | 0 5 0 |
+-------+-------+-------+
| 0 0 9 | 0 4 0 | 3 0 1 |
| 0 0 0 | 7 0 2 | 0 0 0 |
| 0 0 0 | 0 0 8 | 0 0 6 |
+-------+-------+-------+

After:
+-------+-------+-------+
| 3 9 4 | 2 8 5 | 4 6 7 |
| 8 9 5 | 1 6 7 | 2 0 3 |
| 7 2 6 | 9 3 4 | 5 1 8 |
+-------+-------+-------+
| 6 7 3 | 4 5 9 | 1 8 2 |
| 9 5 8 | 6 2 1 | 7 3 4 |
| 4 1 2 | 8 7 3 | 6 5 9 |
+-------+-------+-------+
| 2 8 9 | 5 4 6 | 3 7 1 |
| 1 6 1 | 7 9 2 | 8 4 5 |
| 5 4 7 | 3 1 8 | 9 2 6 |
+-------+-------+-------+
```

- [Tic Tac Toe](https://github.com/KrisNguyen135/AI-Approaches/tree/master/PathFinding/TicTacToe):
minimax + alpha-beta pruning (to be mentioned: chess)
 
## Genetic algorithm
 
Freedom in generating new solutions, only specifications in the fitness
function and how to preserve good individuals.
 
Games:
- [Optimization of polynomials](https://github.com/KrisNguyen135/AI-Approaches/tree/master/GeneticAlgorithm/Optimization):
a form of search, to be compared with other optimization schemes (e.g., 
gradient descent)

<img src="https://github.com/KrisNguyen135/AI-Approaches/blob/master/Media/Optimization/combined.gif" width="400" height="300"/>

- [Jigsaw](https://github.com/KrisNguyen135/AI-Approaches/tree/master/GeneticAlgorithm/Jigsaw):
customized, more involved fitness crossover functions

<img src="https://github.com/KrisNguyen135/Genetic-Jigsaw-Solver/blob/master/Media/Jigsaw/combined.gif" width="300" height="300"/>

- [Traveling salesman](https://github.com/KrisNguyen135/AI-Approaches/tree/master/GeneticAlgorithm/TravelingSalesman):
elitism and ordered crossover
 
## Reinforcement learning
 
Self-exploring agents, only specifications in the scoring function, using
Q-learning.
 
Games: 
- [Nim (revisited)](https://github.com/KrisNguyen135/AI-Approaches/tree/master/ReinforcementLearning/Nim):
Q-value matrix (to be mentioned: the requirement of good opponents)
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
