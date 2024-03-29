# import Pendulum_lc as Pd

import CMGDB_util
import CMGDB
import RoA
import dyn_tools
import Grid

import Ackermann

import TimeMap

import numpy as np

import matplotlib.pyplot as plt

from datetime import datetime

sb = 20
time = 10  # time in seconds

MG_util = CMGDB_util.CMGDB_util()


# TM = TimeMap.TimeMap("ackermann_lc", time,
#                      "examples/tripods/ackermann_lc.yaml")


# subdiv_min = 10  # minimal subdivision to compute Morse Graph
# subdiv_max = 10  # maximal subdivision to compute Morse Graph

subdiv_init = subdiv_min = subdiv_max = sb  # non adaptive proceedure

N = 300  # total of points to plot graphs

# POSITION_BOUNDS
x_min = -10  # -2
x_max = 10  #
y_min = -10  # -1
y_max = 10  # 2

VEL_BOUNDS = 1  # size of the box with the center at the goal (velocity)
THETA_BOUND = 3.14159  # np.pi

# base name for the output files.
base_name = "learned_ack_time" + \
    str(time) + "_" + \
    str(subdiv_init)


print(base_name)


# ### Loading functions


# Graphs
# x_cube = MG_util.sample_points([x_min, y_min, -THETA_BOUND],
#                                [x_max, y_max, THETA_BOUND], N)


# Ack = Ackermann.Ackermann(ctrl_type="learned")
# Ack.plot_graphs(g, x_cube, base_name, save=True)


# Define the parameters for CMGDB
lower_bounds = [x_min, y_min, -THETA_BOUND]
upper_bounds = [x_max, y_max, THETA_BOUND]


# load map

grid = Grid.Grid(lower_bounds, upper_bounds, sb, base_name=base_name)

startTime = datetime.now()

file_name = base_name + "_map_grid.csv"
map = grid.load_map_grid(file_name, lower_bounds, upper_bounds, sb)

print(f"Time to load map = {datetime.now() - startTime}")


def g_on_grid(x):
    return grid.image_of_vertex_from_loaded_map(map, x, lower_bounds, upper_bounds, sb)


phase_periodic = [False, False, True]

K = 1.05


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
