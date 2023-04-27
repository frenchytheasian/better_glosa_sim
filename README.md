# Predictive Cruise Control (PCC) SUMO siimulations

This repository contains python code for the creation of SUMO simulations. I am trying to run analysis on different scenarios in which vehicles have predictive cruise control capagilities with relationship to the upcoming traffic signals. This was done for Dr. Ismail's CS490 Advanced Wireless Sensor Networks class

# Instructions for Running

## Pre-requisites

- [Python](https://www.python.org/)
- [SUMO](https://sumo.dlr.de/docs/Installing/index.html)

## Setup

```bash
pip install -r requirements.txt
```

## Running

```bash
python runner.py
```

### Options

[--intersections] int: Number of intersections to include in the simulation

[--seed] int: Seed for the randomization

[--distance_between] int: Distance between all of the stoplights

[--filename] str: The name of the network files

[--nogui] bool: Whether or not to run the simulation without the gui

## Viewing Output

```bash
python graph.py
```

## For class

The file "project.py" contains the code I wrote to run the program for my project
