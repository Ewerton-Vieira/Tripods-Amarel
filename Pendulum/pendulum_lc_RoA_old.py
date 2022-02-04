# import Pendulum_lc as Pd

import CMGDB_util
import CMGDB
import RoA
import dyn_tools
import Grid
import sys

import TimeMap

import numpy as np

import matplotlib.pyplot as plt

from datetime import datetime

MG_util = CMGDB_util.CMGDB_util()


sb = 20
time = 1  # time is equal to 10s

# subdiv_min = 10  # minimal subdivision to compute Morse Graph
# subdiv_max = 10  # maximal subdivision to compute Morse Graph
subdiv_init = subdiv_min = subdiv_max = sb  # non adaptive proceedure


x_min = -3.14159
x_max = 3.14159

y_min = -6.28318
y_max = 6.28318


# base name for the output files.
base_name = "learned_pendulum_time" + \
    str(time) + "_" + \
    str(subdiv_init)


print(base_name)


# Define the parameters for CMGDB
lower_bounds = [x_min, y_min]
upper_bounds = [x_max, y_max]


# load map

grid = Grid.Grid(lower_bounds, upper_bounds, sb, base_name=base_name)

file_name = base_name + "_map_grid.csv"
map = grid.load_map_grid(file_name, lower_bounds, upper_bounds, sb)


def g_on_grid(x):
    return grid.image_of_vertex_from_loaded_map(map, x, lower_bounds, upper_bounds, sb)


phase_periodic = [True, False]


K = 2


def F(rect):
    # return CMGDB.BoxMap(g_on_grid, rect, padding=True)
    # return MG_util.F_K(g_on_grid, rect, K)
    return MG_util.BoxMapK(g_on_grid, rect, K)


morse_graph, map_graph = MG_util.run_CMGDB(
    subdiv_min, subdiv_max, lower_bounds, upper_bounds, phase_periodic, F, base_name, subdiv_init)

startTime = datetime.now()

roa = RoA.RoA(map_graph, morse_graph)

print(f"Time to build the regions of attraction = {datetime.now() - startTime}")

roa.save_file(base_name)
