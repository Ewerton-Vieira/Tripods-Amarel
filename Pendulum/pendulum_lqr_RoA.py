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


sb = 12
time = 1 - 0.1  # time is equal to 10s

# subdiv_min = 10  # minimal subdivision to compute Morse Graph
# subdiv_max = 10  # maximal subdivision to compute Morse Graph
subdiv_init = subdiv_min = subdiv_max = sb  # non adaptive proceedure


x_min = -3.14159
x_max = 3.14159

y_min = -6.28318
y_max = 6.28318


# base name for the output files.
base_name = "pendulum_lqr_time" + \
    str(time) + "_" + \
    str(subdiv_init)


print(base_name)


# Define the parameters for CMGDB
lower_bounds = [x_min, y_min]
upper_bounds = [x_max, y_max]


# load map
# set the time step
TM = TimeMap.TimeMap("pendulum_lc", time,
                     "examples/tripods/lc_roa.yaml")

# define the lqr time map for the pendulum


def g(X):
    Y = TM.pendulum_lqr(X)
    return Y


phase_periodic = [True, False]

# without noise in t
K = [1.16, 1.16]
noise = [0.1, 0.1]

# #with noise in t
# K = [1.16, 1.16]
# noise = [0.25, 0.1]


def F(rect):
    # return CMGDB.BoxMap(g, rect, padding=True)
    # return MG_util.F_K(g, rect, K)
    # return MG_util.BoxMapK(g_on_grid, rect, K)
    return MG_util.Box_noisy_K(g, rect, K, noise)


morse_graph, map_graph = MG_util.run_CMGDB(
    subdiv_min, subdiv_max, lower_bounds, upper_bounds, phase_periodic, F, base_name, subdiv_init)

# CMGDB.PlotMorseSets(morse_graph)

startTime = datetime.now()

roa = RoA.RoA(map_graph, morse_graph)

print(f"Time to build the regions of attraction = {datetime.now() - startTime}")

roa.save_file(base_name)

fig, ax = roa.PlotTiles()

# RoA.PlotTiles(lower_bounds, upper_bounds,
#               from_file=base_name, from_file_basic=True)

plt.show()

# roa.save_file(base_name)
