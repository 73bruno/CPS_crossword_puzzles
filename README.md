# Constraint Satisfaction Problem Practice Project
This project contains the code and experiments carried out for Practice 1 of the Intelligent Systems course at the University of Alicante during the 2023/2024 academic year.

## Project Overview
The main goal of this practice was to implement and apply constraint satisfaction problem (CSP) solving algorithms to the problem of generating crossword puzzles.

The implementations follow the guidelines specified by the Computer Science and Artificial Intelligence Department at the University of Alicante. The key algorithms covered include:

## AC3 algorithm
Forward Checking algorithm
Each algorithm is applied to sample crossword problems and puzzle generation. Experiments are performed to analyze performance.

## Problem Domain
A crossword puzzle is modeled as a CSP where each letter position is a variable, the domains are possible letters, and constraints specify required letters in overlapping words.

Example problems of varying sizes are provided in text files along with word lists used to populate the puzzles.

## Implementations
Variable, AC3, and Forward Checking classes are implemented from scratch as specified.

The interface allows constructing and editing sample puzzles, then running the solvers. Outputs include variable domains and traces.

## Documentation (in Spanish)
The documentation describes the algorithms, models a small sample problem, and traces solver steps. Experiments analyze solver performance on different puzzle sizes. Time comparisons use graphs.
