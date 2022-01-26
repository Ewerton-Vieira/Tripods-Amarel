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

sb = 18
time = 5000  # time in seconds

TM = TimeMap.TimeMap("ackermann_hyb", time)

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
THETA_BOUND = 3.14159  # np.pi

# base name for the output files.
base_name = "2_hyb_arckermann" + \
    str(time) + "_" + \
    str(subdiv_init)


print(base_name)

#

first_goal = [0, 0, -1.57]  # [0, 0, 1.57]
# intermediate_goal = [-4, -4, -1.57]


def g(X):
    return TM.ackermann_hyb(X)


print("g([4, 4, 1.57])", g([4, 4, 1.57]))

TM.ss.copy_point_from_vector(TM.goal_state, first_goal)
TM.ctrl.set_goal(TM.goal_state)


def g(X):
    TM.ss.copy_point_from_vector(TM.goal_state, first_goal)
    TM.ctrl.set_goal(TM.goal_state)
    return TM.ackermann_hyb(X)
# print("g([4, 4, 1.57])", g([4, 4, 1.57]))
#
# print("g(intermediate_goal)", g(intermediate_goal))
#
# TM.ss.copy_point_from_vector(TM.goal_state, intermediate_goal)
# TM.ctrl.set_goal(TM.goal_state)
#
#
# print("changed goal g([4, 4, 1.57])", g([4, 4, 1.57]))
#
#
# TM.ss.copy_point_from_vector(TM.goal_state, first_goal)
# TM.ctrl.set_goal(TM.goal_state)
#
#
# def g_interm(X):
#     return
#
#
# def g_2(X):
#     Y = g(X)
#
#     # return Y
#     if np.linalg.norm(np.array(Y) - np.array(first_goal)) < 0.01:
#         return Y
#
#     else:
#         # intermediate goal
#         TM.ss.copy_point_from_vector(TM.goal_state, intermediate_goal)
#         TM.ctrl.set_goal(TM.goal_state)
#         # TM.ctrl_2.set_goal(TM.goal_state)
#
#         Y_ = g(X)
#         # goal
#         TM.ss.copy_point_from_vector(TM.goal_state, first_goal)
#         TM.ctrl.set_goal(TM.goal_state)
#         # TM.ctrl_2.set_goal(TM.goal_state)
#
#         return g(Y_)
#
#
# print(g_2([-2, -5, 0]))


# Graphs
x_cube = MG_util.sample_points([x_min, y_min, -THETA_BOUND],
                               [x_max, y_max, THETA_BOUND], N)


Ack.plot_graphs(g, x_cube, base_name, save=False)


# Define the parameters for CMGDB
lower_bounds = [x_min, y_min, -THETA_BOUND]
upper_bounds = [x_max, y_max, THETA_BOUND]


phase_periodic = [False, False, True]

# K = sampled_Lipschitz(lower_bounds, upper_bounds, N, g, base_name)
K = [1.05, 1.05, 1.05]


def F(rect):
    return MG_util.F_K(rect, g, K)


morse_graph, map_graph = MG_util.run_CMGDB(
    subdiv_min, subdiv_max, lower_bounds, upper_bounds, phase_periodic, F, base_name, subdiv_init)

startTime = datetime.now()

DG = RoA.Domain_Graph(map_graph, morse_graph)

print(f"Time to build the ancestors_graph time = {datetime.now() - startTime}")

retract_tiles, retract_indices, morse_nodes_map = DG.morse_retract()

DG.save_file(retract_tiles, retract_indices, base_name)

# plot
fig, ax = RoA.PlotMorseTiles(lower_bounds, upper_bounds, from_file=base_name)

plt.savefig(base_name)
plt.show()


# plot
proj_dims = [0, 1]
name_plot = base_name + "RoA" + str(proj_dims)
DG.PlotOrderRetraction(morse_graph, map_graph, retract_tiles,
                       retract_indices, proj_dims=proj_dims, name_plot=name_plot)

proj_dims = [1, 2]
name_plot = base_name + "RoA" + str(proj_dims)
DG.PlotOrderRetraction(morse_graph, map_graph, retract_tiles,
                       retract_indices, proj_dims=proj_dims, name_plot=name_plot)

proj_dims = [0, 2]
name_plot = base_name + "RoA" + str(proj_dims)
DG.PlotOrderRetraction(morse_graph, map_graph, retract_tiles,
                       retract_indices, proj_dims=proj_dims, name_plot=name_plot)
