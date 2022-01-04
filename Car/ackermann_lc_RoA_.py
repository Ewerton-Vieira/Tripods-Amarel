# import Pendulum_lc as Pd

import CMGDB_util
import CMGDB
import ROA
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


TM = TimeMap.TimeMap("ackermann_lc", time,
                     "examples/tripods/ackermann_lc.yaml")


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


# test
vertex = [(upper_bounds[a] - lower_bounds[a])/(2**(1 + (a & 1))) for a in range(len(upper_bounds))]

print("region, vertex coordinates", grid.vertex2grid_vertex(
    vertex, lower_bounds, upper_bounds, sb))
print(g_on_grid(vertex))


phase_periodic = [False, False, True]

K = 1.05

#
# def F(rect):
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
#
# # plot
# fig, ax = ROA.PlotMorseTiles(lower_bounds, upper_bounds, from_file=base_name)

# plt.savefig(base_name)
# plt.show()


# fig, ax = ROA.PlotMorseTiles(lower_bounds, upper_bounds,
#                              from_file=base_name, from_file_basic=True)
#
# plt.savefig(base_name)
# plt.show()

#
# # plot
# proj_dims = [0, 1]
# name_plot = base_name + "ROA" + str(proj_dims)
# DG.PlotOrderRetraction(morse_graph, map_graph, retract_tiles,
#                        retract_indices, proj_dims=proj_dims, name_plot=name_plot)
#
# proj_dims = [1, 2]
# name_plot = base_name + "ROA" + str(proj_dims)
# DG.PlotOrderRetraction(morse_graph, map_graph, retract_tiles,
#                        retract_indices, proj_dims=proj_dims, name_plot=name_plot)
#
# proj_dims = [0, 2]
# name_plot = base_name + "ROA" + str(proj_dims)
# DG.PlotOrderRetraction(morse_graph, map_graph, retract_tiles,
#                        retract_indices, proj_dims=proj_dims, name_plot=name_plot)
