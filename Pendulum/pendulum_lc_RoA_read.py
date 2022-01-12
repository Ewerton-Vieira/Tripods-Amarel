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

# TM = TimeMap.TimeMap("pendulum_lc", time,
#                      "examples/tripods/lc_roa.yaml")

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


fig, ax = RoA.PlotMorseTiles(lower_bounds, upper_bounds, from_file=base_name)


# fig, ax = RoA.PlotMorseTiles(lower_bounds, upper_bounds,
#                              from_file=base_name, from_file_basic=True)


# dynamics

TM1 = TimeMap.TimeMap("pendulum_lc", 0.01,
                      "examples/tripods/lc_roa.yaml")

fig, ax = dyn_tools.Plot_trajectories(lower_bounds, upper_bounds, TM1.pendulum_lc, fig=fig, ax=ax, xlim=[
                                      lower_bounds[0], upper_bounds[0]], ylim=[lower_bounds[1], upper_bounds[1]])

plt.savefig(base_name)
plt.show()
