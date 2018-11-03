# Maze-Solver

A small program that can find the optimal solution to (almost) any maze. The maze has to conform to the specifications below in order for maze-solver to be able to solve it. The solved maze will be outputted in image form, with the optimal path drawn in blue.

## Usage
How to get the project up and running on your own computer

### Prerequisites
This project is compatible with Python 3.x. For large mazes, a 64bit installation is recommended so that more than 2GB of RAM can be utilized. 

For image processing the project uses [Pillow](https://github.com/python-pillow/Pillow), which you can install using pip:

```
pip install pillow
```

No installation is required. Simply clone this repository to your machine and run `main.py` from the command line.

## Running
Run `main.py` with arguments for input (and optionally) output paths, as well as which conversion and solving algorithms to use.

```
python3 main.py input.png -o output.png -c scan -s dijkstra
```

Use the flag `-h` for detailed instructions on how to run the program. 

### Currently implemented search algorithms
1. Dijkstra

### Currently implemented conversion algorithms
1. Scan
2. Traversal

## Maze requirements
In order for `maze-solver` to be able to process a maze, it must adhere to the following requrements: 

1. Must be in PNG form
2. Walls and corridors must be 1px wide, with walls being black and corridors being white
3. There must be only one entrance and exit
