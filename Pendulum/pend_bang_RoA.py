import CMGDB_util
import CMGDB
import RoA
import dyn_tools
import Grid
import sys

import NoisyTimeMap

import numpy as np

import matplotlib.pyplot as plt

from datetime import datetime

MG_util = CMGDB_util.CMGDB_util()


sb = 12
time = 1  # time is equal to time * 0.1s
ctrl_num = 2

# subdiv_min = 10  # minimal subdivision to compute Morse Graph
# subdiv_max = 10  # maximal subdivision to compute Morse Graph
subdiv_init = subdiv_min = subdiv_max = sb  # non adaptive proceedure


# base name for the output files.
base_name = "pend_bang" + \
    str(ctrl_num) + "_" + str(time) + "_" + \
    str(subdiv_init)


print(base_name)

# load map
# set the time step
TM = NoisyTimeMap.NoisyTimeMap("examples/tripods/pendulum_noise.yaml")
TM.duration = time
# define the lqr time map for the pendulum


# Define the parameters for CMGDB
TM.ss.print_bounds()
lower_bounds = TM.ss.get_lower_bounds()
upper_bounds = TM.ss.get_upper_bounds()

print(lower_bounds, upper_bounds)


def g(X):
    return TM.pendulum_bang_bang(X, ctrl_num=ctrl_num)


print(g([0, 0]))

phase_periodic = [True, False]


def F(rect):
    return CMGDB.BoxMap(g, rect, padding=False)


morse_graph, map_graph = MG_util.run_CMGDB(
    subdiv_min, subdiv_max, lower_bounds, upper_bounds, phase_periodic, F, base_name, subdiv_init)

# CMGDB.PlotMorseSets(morse_graph)

startTime = datetime.now()

roa = RoA.RoA(map_graph, morse_graph)

print(f"Time to build the regions of attraction = {datetime.now() - startTime}")

roa.save_file(base_name)

fig, ax = roa.PlotTiles()

# # TM1 = NoisyTimeMap.NoisyTimeMap("examples/tripods/pendulum_noise.yaml")
# #
# TM.duration = 0.1
#
# fig, ax = dyn_tools.Plot_trajectories(lower_bounds, upper_bounds, g, fig=fig, ax=ax, xlim=[
#                                       lower_bounds[0], upper_bounds[0]], ylim=[lower_bounds[1], upper_bounds[1]])

# RoA.PlotTiles(lower_bounds, upper_bounds,
#               from_file=base_name, from_file_basic=True)

ax.set_xlabel(r"$\theta$")
ax.set_ylabel(r"$\dot \theta$")
plt.savefig(base_name, bbox_inches='tight')
plt.show()

# roa.save_file(base_name)
