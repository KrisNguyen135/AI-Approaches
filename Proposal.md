# Title: _AI Approaches to Classic Games_
Subtitle: _Hands-on implementation of intelligent systems in the adversarial
context of classic games_

Alternative titles:
- AI-based Problem Solving in Python
- Python Artificial Intelligence in Classic Games

## Introduction
Artificial intelligence has been one of the fastest growing subfields of
computer science in recent years, but its history is more extensive than that.
Going from path-finding algorithms such as depth-first-search and breadth-first
search to evolutionarily-inspired genetic algorithms, reinforcement learning
for gaming agents, and finally to machine learning and deep neural network
models, the history of AI has seen a wide range of variations in terms of ideas
and approaches. With that said, for this reason, the field can also be quite
intimidating for newcomers who would like to understand the fundamental
concepts mentioned above.

_AI Approaches to Classic Games_ serves as a comprehensive guide that walks its
readers through those concepts in an incremental way. Starting from low-level,
hands-on algorithms such as hard-coded logic and path-finding algorithms, the
book introduces the idea of artificial intelligence in the simplest sense and
builds up from there to more complex, general-purpose models using machine
learning and deep learning.

Additionally, by framing the discussions in the context of solving classic
games such as Mine Sweeper, Nim, Sudoku and Snake in an automated way, the book
offers a unique domain to design and implement AI systems. Games are isolated,
self-contained environments where clear actions and goals are already
determined. By discussing how to design agents that can automatically interact
with and win these games, we can explore the capabilities of AI systems in an
engaging way and finally extrapolate them to real-life applications.

All the code that implements the games and the AI agents in the book will be in
Python. The Python programming language is one of the most popular and
versatile tools to design and proptotype computer systems, and by pairing the
theoretical discussions in the book with the corresponding Python programming
exercises, the book offers a hands-on approach to learning about these AI
topics. By the end of the book, readers will obtain a deep understanding on the
discussed fundamental AI ideas as well as a working knowledge on how to
implement them in Python.

## Target audience
__Who is the audience?__
- Computer Science students and Python enthusiasts looking to learn more about
important, fundamental concepts in Artificial Intelligence.
- AI students who would like to solidify their knowledge in the hands-on
context of automatic game playing.
- AI researchers who would like to explore specific adversarial environments to
test out their AI agents.

__What should the audience have before starting?__
- Basic knowledge on general programming.
- Relative experience with Python, including working with classes, lists, NumPy
arrays, as well as visualizations with Matplotlib.
 
__What will the audience gain at the end?__
- A theoretical understanding of AI concepts such as search algorithms, genetic
algorithm, reinforcement learning, machine learning and neural networks, as
well as the incremental increase in their complexity and capabilities.
- Knowledge on how to train agents to automatically interact with and beat
games by leveraging those AI concepts.
- Hands-on experience of implementing and analyzing AI models using Python and
popular scientific libraries such as NumPy, Matplotlib, Scikit-learn and
PyTorch.

## Tentative structure
We will go through the following topics in order, so that we can observe the
increasing order of complexity in the models, together with the capabilities in
interacting with the games.

### Hard-coded logic
This section explores the lowest level of implementing intelligent systems:
specifically designed programs. By hard-coding what a model should do in
specific situations, we will discuss the most basic idea of artificial
intelligence, while introducing the readers to the general structure of
individual topics in the book.

The following games will be covered:
- [Nim](https://en.wikipedia.org/wiki/Nim): Players take turn to remove certain
numbers of items from a heap. Whoever takes the last item from the heap wins.
We will be discussing the perfect strategy for this game and implementing it in
a Python program.
- [Minesweeper](https://en.wikipedia.org/wiki/Minesweeper_(video_game\)):
Clearing a board while avoiding hidden mines.
[![IMAGE ALT TEXT](http://img.youtube.com/vi/2MEV2SVbZJ4/0.jpg)](https://www.youtube.com/watch?v=2MEV2SVbZJ4 "Automated Minesweeper")

### Path-finding algorithms
This second section of the book goes into the topic of searching for optimal
solutions via various strategies including depth-first-search,
breadth-first-search, minimax and alpha-beta. By formalizing the process of
finding optimal solutions to games such as Maze, Sudoku and Tic Tac Toe via
algorithmic processes, we will transition to learning models that have a higher
level of generalization that hard-coded algorithms from the earlier section.

The following games will be covered:
- [Maze](https://en.wikipedia.org/wiki/Maze): Finding a clear path going from a
given starting point to the destination.
![Maze Alt Text](https://github.com/KrisNguyen135/AI-Approaches/blob/master/Media/Maze/combined.gif)
- [Sudoku](https://en.wikipedia.org/wiki/Sudoku): Completing a 9 by 9 grid with
digits so that each column, each row, and each of the 3 by 3 sub-grids contain
all of the digits from 1 to 9.
- [Tic Tac Toe](https://en.wikipedia.org/wiki/Tic-tac-toe): Players take turn
to try to fill an entire row, column or diagonal with either X's or O's.

### Genetic algorithms
Genetic algorithms denote a certain evolution-inspired approach to optimization
problems. By structuring the workflow of a search with aspects of an
evolutionary process such as crossover, mutation and selection, genetic
algorithms offer a unique method of modeling and finding optimal solutions to
specific problems.

The following games will be covered:
- [Jigsaw puzzles](https://en.wikipedia.org/wiki/Jigsaw_puzzle): Ordering small
pieces of a large picture in the correct arrangement to assemble the complete
picture.
![Jigsaw Alt Text](https://github.com/KrisNguyen135/AI-Approaches/blob/master/Media/Jigsaw/combined.gif)
- [The travelling salesman problem](https://en.wikipedia.org/wiki/Travelling_salesman_problem):
The famous mathematical problem of finding the shortest possible path that goes
through all elements of a given set of locations.
![Travel Alt Text](https://github.com/KrisNguyen135/AI-Approaches/blob/master/Media/TravelingSalesman/combined.gif)

### Reinforcement learning
Reinforcement learning (RL) is one of the most popular forms of AI design that
allows an agent to explore the given environment via trial and error, thus
gathering information that will help inform its future decisions. A typical RL
workflow will contain various concepts such as state, reward and policy.

![RL Alt Text](https://www.kdnuggets.com/images/reinforcement-learning-fig1-700.jpg)

These topics will be explained and applied in the following games:
- [Nim](https://en.wikipedia.org/wiki/Nim) (revisited): By considering the
application of RL to the game of Nim, we will be able to observe the increase
in capability going from a specifically designed model (as discussed in the
first section) to an RL agent.
- [Snake](https://en.wikipedia.org/wiki/Snake_(video_game_genre\)): Controlling
a snake agent to avoid obstacle and find food rewards.

### Machine learning
Machine learning (ML) has been one of the most popular AI approaches in a wide
range of problems in recent years. Machine learning models rely on various
strategies of data analysis to detect patterns and trends and extrapolate from
their training data. We will be covering two of the most popular ML models:
Support Vector Machine and neural networks.

The following games will be covered:
- [Tic Tac Toe](https://en.wikipedia.org/wiki/Tic-tac-toe): Players take turn
to mark the cells in a 3 by 3 grid. The goal is to create three of the same
marks in the same horizontal, vertical or diagonal row.
- [Nim](https://en.wikipedia.org/wiki/Nim) (revisited): Nim is again used to
illustrate the differences between various AI approaches. This time, we will
be able to see the capability of generalizing from past data of an ML model.

### Exotic deep learning
Being a special type of machine learning model with a unique structure and
learning capability, neural networks are often combined with other classical
AI approaches to either accelerate their training time or optimize for a unique
task. In this section, we will consider two such approaches: NEAT
(NeuroEvolution of Augmenting Topologies - a genetic algorithm take on
designing the structure of neural networks) and Deep Q-Learning (the
combination between deep learning and reinforcement learning).

The following games will be covered:
- [Flappy Birds](https://en.wikipedia.org/wiki/Flappy_Bird): Controlling a
flying agent to avoid obstacles by tapping on the screen.
[![IMAGE ALT TEXT](http://img.youtube.com/vi/PjhmkJBUuVU/0.jpg)](https://www.youtube.com/watch?v=PjhmkJBUuVU "NEAT in Flappy Bird")
- [Snake](https://en.wikipedia.org/wiki/Snake_(video_game_genre\)) (revisited):
In this environment of the Snake game, we will have our AI model take in the
most general, non-engineered form of input: the actual game graphical pictures. 
