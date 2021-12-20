# import Pendulum_lc as Pd

import CMGDB_util
import CMGDB
import ROA
import dyn_tools

import Ackermann

import TimeMap

import numpy as np

import matplotlib.pyplot as plt

from datetime import datetime

sb = 14
time = 5  # step is equal to STEP * 0.1s

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


def g(X):
    return TM.ackermann_lc(X)


print(g([-10, -10, 2.0944]))


# Graphs
x_cube = MG_util.sample_points([x_min, y_min, -THETA_BOUND],
                               [x_max, y_max, THETA_BOUND], N)


Ack = Ackermann.Ackermann(ctrl_type="learned")
Ack.plot_graphs(g, x_cube, base_name, save=True)


# Define the parameters for CMGDB
lower_bounds = [x_min, y_min, -THETA_BOUND]
upper_bounds = [x_max, y_max, THETA_BOUND]


phase_periodic = [False, False, True]

K = [1.05, 1.05, 1.05]


def F(rect):
    return MG_util.F_K(rect, g, K)


morse_graph, map_graph = MG_util.run_CMGDB(
    subdiv_min, subdiv_max, lower_bounds, upper_bounds, phase_periodic, F, base_name, subdiv_init)

startTime = datetime.now()

DG = ROA.Domain_Graph(map_graph, morse_graph)

print(f"Time to build the ancestors_graph time = {datetime.now() - startTime}")

retract_tiles, retract_indices, morse_nodes_map = DG.morse_retract()

DG.save_file(retract_tiles, retract_indices, base_name)

# plot
fig, ax = ROA.PlotMorseTiles(lower_bounds, upper_bounds, from_file=base_name)

plt.savefig(base_name)
plt.show()


# plot
proj_dims = [0, 1]
name_plot = base_name + "ROA" + str(proj_dims)
DG.PlotOrderRetraction(morse_graph, map_graph, retract_tiles,
                       retract_indices, proj_dims=proj_dims, name_plot=name_plot)

proj_dims = [1, 2]
name_plot = base_name + "ROA" + str(proj_dims)
DG.PlotOrderRetraction(morse_graph, map_graph, retract_tiles,
                       retract_indices, proj_dims=proj_dims, name_plot=name_plot)

proj_dims = [0, 2]
name_plot = base_name + "ROA" + str(proj_dims)
DG.PlotOrderRetraction(morse_graph, map_graph, retract_tiles,
                       retract_indices, proj_dims=proj_dims, name_plot=name_plot)
