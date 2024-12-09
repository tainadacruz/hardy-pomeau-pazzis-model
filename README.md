# HPP Cellular Automaton with Moore's Neighborhood

## Description
This Python script simulates the HPP (Hardy-Pomeau-Pomeau) cellular automaton, implementing a 2D grid with Moore's neighborhood. The automaton models basic fluid dynamics using simple rules of particle movement and collision.

The simulation considers particles moving in **eight directions** (up, down, left, right, and diagonals) on a 2D grid. At each step, particles move (streaming) and interact (collision) according to predefined rules. The system ensures periodic boundary conditions, so particles exiting one side of the grid re-enter from the opposite side.

The visualization provides an animated display of the particle density across the grid over time.

## Features
- **Moore's Neighborhood**: Movement and collision rules account for all eight directions around each cell.
- **Periodic Boundary Conditions**: Particles leaving one edge of the grid reappear on the opposite side.
- **Dynamic Visualization**: Uses Matplotlib to animate particle density over simulation steps.
- **Conservation of Particles**: Implements rules to maintain the total number of particles across the grid.

## Purpose
This project is an assignment for the **INE5425** subject entitled **Modeling and Simulation (INE5425)** in the computer science course at the **Federal University of Santa Catarina (UFSC)**.

## Requirements
- Python 3.7 or later
- Required libraries: `numpy` and `matplotlib`

### Installation
Install the necessary packages by running:
```bash
pip install numpy matplotlib
```

### How to run
Run the script using Python:
```bash
python automaton_simulation.py
```

### How It Works
- **Initialization**: Particles are randomly distributed in a circular region of the grid with equal probabilities for each direction.
- **Streaming**: Particles move in their current directions, considering periodic boundary conditions.
- **Collision**: Particles in the same cell interact based on the number and configuration of particles, redistributing directions to maintain total particle count.
- **Visualization**: The simulation is displayed as an animated heatmap, where the color intensity represents particle density.