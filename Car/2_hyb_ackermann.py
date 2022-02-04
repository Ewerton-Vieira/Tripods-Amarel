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
import libpyDirtMP as prx

import Lips
import RoA
import CMGDB_util


# Functions defined by LQR or Motion planner
Ack = Ackermann.Ackermann()
MG_util = CMGDB_util.CMGDB_util()

sb = 16
time = 10000  # time in seconds

TM = TimeMap.TimeMap("ackermann_hyb", time)

# subdiv_min = 10  # minimal subdivision to compute Morse Graph
# subdiv_max = 10  # maximal subdivision to compute Morse Graph
subdiv_init = subdiv_min = subdiv_max = sb  # non adaptive proceedure

N = 1000000  # total of points to plot graphs

# POSITION_BOUNDS
x_min = -10
x_max = 10
y_min = -10
y_max = 10


VEL_BOUNDS = 1  # size of the box with the center at the goal (velocity)
THETA_BOUND = 3.14159  # np.pi

# base name for the output files.
base_name = "2_hyb_arckermann" + \
    str(time) + "_" + \
    str(subdiv_init)


print(base_name)

#

goal = [0, 0, 1.57]  # [0, 0, 1.57]
intermediate_goal = [6, -10, -1.57]

TM.ss.copy_point_from_vector(TM.goal_state, goal)


def g(X):
    return TM.ackermann_hyb(X)


def g_2(X):
    TM.ss.copy_point_from_vector(TM.goal_state, goal)
    Y = TM.ackermann_hyb(X)

    # return Y
    if np.linalg.norm(np.array(Y) - np.array(goal)) < 0.1:
        return Y

    else:

        # intermediate goal
        TM.ss.copy_point_from_vector(TM.goal_state, intermediate_goal)
        Y_ = TM.ackermann_hyb(X)

        # goal
        TM.ss.copy_point_from_vector(TM.goal_state, goal)

        return TM.ackermann_hyb(Y_)

#
# print(g_2([-2, -5, 0]))


# Graphs
x_cube = MG_util.sample_points([x_min, y_min, -THETA_BOUND],
                               [x_max, y_max, THETA_BOUND], N)


Ack.plot_graphs(g_2, x_cube, base_name, goal=goal, save=True)


# Define the parameters for CMGDB
lower_bounds = [x_min, y_min, -THETA_BOUND]
upper_bounds = [x_max, y_max, THETA_BOUND]


phase_periodic = [False, False, True]


def F(rect):
    return CMGDB.BoxMap(g_2, rect, padding=True)


morse_graph, map_graph = MG_util.run_CMGDB(
    subdiv_min, subdiv_max, lower_bounds, upper_bounds, phase_periodic, F, base_name, subdiv_init)

startTime = datetime.now()

roa = RoA.RoA(map_graph, morse_graph)

print(f"Time to build the regions of attraction = {datetime.now() - startTime}")

roa.save_file(base_name)
