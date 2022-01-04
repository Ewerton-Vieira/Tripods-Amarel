# import Pendulum_lc as Pd

import CMGDB_util
import CMGDB
import ROA
import dyn_tools

import TimeMap

import numpy as np

import matplotlib.pyplot as plt

from datetime import datetime


MG_util = CMGDB_util.CMGDB_util()


sb = 12
time = 5  # time is equal to 10s

TM = TimeMap.TimeMap("pendulum_lc", time,
                     "examples/tripods/lc_roa.yaml")

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


# ### Loading functions

#
# def g(X):
#     return TM.pendulum_lc(X)
#
#
# print(g([0.6, 0.6]))


# Define the parameters for CMGDB
lower_bounds = [x_min, y_min]
upper_bounds = [x_max, y_max]


# load map

startTime = datetime.now()

file_name = base_name + ".csv"
map = grid.load_map_grid(file_name, lower_bounds, upper_bounds, sb)

print(f"Time to load map = {datetime.now() - startTime}")


def g_on_grid(x):
    return grid.image_of_vertex_from_loaded_map(map, x, lower_bounds, upper_bounds, sb)


# test
vertex = [(upper_bounds[a] - lower_bounds[a])/(2**(1 + (a & 1))) for a in range(len(upper_bounds))]

print("region, vertex coordinates", grid.vertex2grid_vertex(
    vertex, lower_bounds, upper_bounds, sb))
print(g_on_grid(vertex))


phase_periodic = [True, False]


K = 1.05


# def F(rect):
#     # return CMGDB.BoxMap(g, rect, padding=True)
#     return MG_util.F_K(rect, g, K)
#
#
# morse_graph, map_graph = MG_util.run_CMGDB(
#     subdiv_min, subdiv_max, lower_bounds, upper_bounds, phase_periodic, F, base_name, subdiv_init)
#
# startTime = datetime.now()
#
# DG = ROA.Domain_Graph(map_graph, morse_graph)
#
# print(f"Time to build the ancestors_graph time = {datetime.now() - startTime}")
#
# retract_tiles, retract_indices, morse_nodes_map = DG.morse_retract()
#
# DG.save_file(retract_tiles, retract_indices, base_name)


# fig, ax = ROA.PlotMorseTiles(lower_bounds, upper_bounds, from_file=base_name)

# fig, ax = ROA.PlotMorseTiles(lower_bounds, upper_bounds,
#                              from_file=base_name, from_file_basic=True)


# # dynamics
#
# TM1 = TimeMap.TimeMap("pendulum_lc", 0.01,
#                       "examples/tripods/lc_roa.yaml")
#
# fig, ax = dyn_tools.Plot_trajectories(lower_bounds, upper_bounds, TM1.pendulum_lc, fig=fig, ax=ax, xlim=[
#                                       lower_bounds[0], upper_bounds[0]], ylim=[lower_bounds[1], upper_bounds[1]])
#
# plt.savefig(base_name)
# plt.show()
