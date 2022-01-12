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

import Lips
import RoA
import CMGDB_util


# Functions defined by LQR or Motion planner

sb = 18
time = 10  # time in seconds

TM = TimeMap.TimeMap("ackermann_hyb", time,
                     "examples/tripods/ackermann_ha_roa.yaml")

# subdiv_min = 10  # minimal subdivision to compute Morse Graph
# subdiv_max = 10  # maximal subdivision to compute Morse Graph
subdiv_init = subdiv_min = subdiv_max = sb  # non adaptive proceedure

N = 500  # total of points to plot graphs

# POSITION_BOUNDS
x_min = -300  # -2
x_max = 300  #
y_min = -300  # -1
y_max = 300  # 2

x_min = -10
x_max = 10
y_min = -10
y_max = 10
#
# x_min = -1
# x_max = 1
# y_min = -1
# y_max = 1

VEL_BOUNDS = 1  # size of the box with the center at the goal (velocity)
THETA_BOUND = 3.14159  # np.pi

# base name for the output files.
base_name = "hyb_arckermann" + \
    str(time) + str([int(x_min), int(y_min), int(x_max), int(y_max)]) + "_" + \
    str(subdiv_init)


print(base_name)

#


def g(X):
    return TM.ackermann_hyb(X)


print(g([-2, -5, 0]))


# Graphs
x_cube = MG_util.sample_points([x_min, y_min, -THETA_BOUND],
                               [x_max, y_max, THETA_BOUND], N)


Ack = Ackermann.Ackermann()
# Ack.plot_graphs(g, x_cube, base_name, save=True)


# Define the parameters for CMGDB
lower_bounds = [x_min, y_min, -THETA_BOUND]
upper_bounds = [x_max, y_max, THETA_BOUND]


phase_periodic = [False, False, True]

# K = sampled_Lipschitz(lower_bounds, upper_bounds, N, g, base_name)
K = [1.05, 1.05, 1.05]


# def F(rect):
#     return MG_util.F_K(rect, g, K)
#
#
# morse_graph, map_graph = MG_util.run_CMGDB(
#     subdiv_min, subdiv_max, lower_bounds, upper_bounds, phase_periodic, F, base_name, subdiv_init)
#
# startTime = datetime.now()
#
# DG = RoA.Domain_Graph(map_graph, morse_graph)
#
# print(f"Time to build the ancestors_graph time = {datetime.now() - startTime}")
#
# retract_tiles, retract_indices, morse_nodes_map = DG.morse_retract()
#
# DG.save_file(retract_tiles, retract_indices, base_name)


# DG.PlotMorseTiles(from_file=base_name)

# RoA.PlotMorseTiles(lower_bounds, upper_bounds, from_file=base_name, plot_point=True)

RoA.PlotMorseTiles(lower_bounds, upper_bounds, from_file=base_name, section=([2], (0, 0, 1.57)))
plt.show()

# proj_dims = [0, 1]
# name_plot = base_name + "RoA" + str(proj_dims)
# DG.PlotOrderRetraction(morse_graph, map_graph, retract_tiles,
#                        retract_indices, proj_dims=proj_dims, name_plot=name_plot)
#
# proj_dims = [1, 2]
# name_plot = base_name + "RoA" + str(proj_dims)
# DG.PlotOrderRetraction(morse_graph, map_graph, retract_tiles,
#                        retract_indices, proj_dims=proj_dims, name_plot=name_plot)
#
# proj_dims = [0, 2]
# name_plot = base_name + "RoA" + str(proj_dims)
# DG.PlotOrderRetraction(morse_graph, map_graph, retract_tiles,
#                        retract_indices, proj_dims=proj_dims, name_plot=name_plot)
