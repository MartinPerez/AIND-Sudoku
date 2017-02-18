# Artificial Intelligence Nanodegree
## Introductory Project: Diagonal Sudoku Solver

# Question 1 (Naked Twins)
Q: How do we use constraint propagation to solve the naked twins problem?  
A: The naked twins can be seen as an extension of the trivial elimination technique. By definition of the constraint that no two boxes can have the same value in a unit, we know that if n boxes out of m boxes in a unit contain exactly the same n possible values, then branching the possibilities would never allow those values to be contained in the other (m - n) boxes. The naked twins strategy would be the case when n=2 while the elimination strategy is the case n=1. This could make sense only up to n=(m - 2), since n=(m - 1) would be a corner case of the only choice strategy.

# Question 2 (Diagonal Sudoku)
Q: How do we use constraint propagation to solve the diagonal sudoku problem?  
A: We represent the box constraints by taking into account the values of their peers. Where the peers are defined according to some arbitrary group definition like columns, runs or squares, that we call units. So we simply add the diagonal as another unit to automatically use it when iterating on the constraints "units" when executing the different strategies.

### Install

This project requires **Python 3**.

We recommend students install [Anaconda](https://www.continuum.io/downloads), a pre-packaged Python distribution that contains all of the necessary libraries and software for this project. 
Please try using the environment we provided in the Anaconda lesson of the Nanodegree.

##### Optional: Pygame

Optionally, you can also install pygame if you want to see your visualization. If you've followed our instructions for setting up our conda environment, you should be all set.

If not, please see how to download pygame [here](http://www.pygame.org/download.shtml).

### Code

* `solutions.py` - You'll fill this in as part of your solution.
* `solution_test.py` - Do not modify this. You can test your solution by running `python solution_test.py`.
* `PySudoku.py` - Do not modify this. This is code for visualizing your solution.
* `visualize.py` - Do not modify this. This is code for visualizing your solution.

### Visualizing

To visualize your solution, please only assign values to the values_dict using the ```assign_values``` function provided in solution.py

### Data

The data consists of a text file of diagonal sudokus for you to solve.
