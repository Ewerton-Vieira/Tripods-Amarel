import CMGDB
import libpyDirtMP

import matplotlib.pyplot as plt
import matplotlib
import numpy as np
import time
import math
import csv
import os
import itertools
from datetime import datetime
import torch

import Ackermann
import TimeMap

import RoA
import CMGDB_util


MG_util = CMGDB_util.CMGDB_util()
# Functions defined by LQR or Motion planner

sb = 20
time = 5  # time in seconds

TM = TimeMap.TimeMap("ackermann_hyb", time,
                     "examples/tripods/ackermann_ha_roa.yaml")

# subdiv_min = 10  # minimal subdivision to compute Morse Graph
# subdiv_max = 10  # maximal subdivision to compute Morse Graph
subdiv_init = subdiv_min = subdiv_max = sb  # non adaptive proceedure

N = 1000  # total of points to plot graphs

# POSITION_BOUNDS

x_min = -10
x_max = 10
y_min = -10
y_max = 10


VEL_BOUNDS = 1  # size of the box with the center at the goal (velocity)
THETA_BOUND = 3.141592653589793  # np.pi


goal = [6, -10, -1.57]

# base name for the output files.

if goal:
    base_name = "hyb_arckermann" + \
        str(time) + "_" + \
        str(subdiv_init) + "interm"

    TM.ss.copy_point_from_vector(TM.goal_state, goal)

else:
    base_name = "hyb_arckermann" + \
        str(time) + "_" + \
        str(subdiv_init)


print(base_name)


def g(X):
    return TM.ackermann_hyb(X)


# Graphs
# x_cube = MG_util.sample_points([x_min, y_min, -THETA_BOUND],
#                                [x_max, y_max, THETA_BOUND], N)


# Ack = Ackermann.Ackermann()
# Ack.plot_graphs(g, x_cube, base_name, goal=goal save=False)


# Define the parameters for CMGDB
lower_bounds = [x_min, y_min, -THETA_BOUND]
upper_bounds = [x_max, y_max, THETA_BOUND]


phase_periodic = [False, False, True]


def F(rect):
    return CMGDB.BoxMap(g, rect, padding=True)
    # return MG_util.F_K(g_on_grid, rect, K)
    # return MG_util.BoxMapK(g_on_grid, rect, K)


morse_graph, map_graph = MG_util.run_CMGDB(
    subdiv_min, subdiv_max, lower_bounds, upper_bounds, phase_periodic, F, base_name, subdiv_init)

startTime = datetime.now()

roa = RoA.RoA(map_graph, morse_graph)

print(f"Time to build the regions of attraction = {datetime.now() - startTime}")

roa.save_file(base_name)
