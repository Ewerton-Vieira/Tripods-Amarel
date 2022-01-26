import CMGDB_util
import CMGDB
import RoA
import dyn_tools
import Grid


import numpy as np

import matplotlib.pyplot as plt

from datetime import datetime

sb = 20
time = 5  # time in seconds
STEP = 500

subdiv_init = subdiv_min = subdiv_max = sb  # non adaptive proceedure

# POSITION_BOUNDS
EPSILON_THETAS = pi = 3.141592653589793  # size of the box with the center at the goal (thetas)
EPSILON_DOTS = 6  # 6  # size of the box with the center at the goal (thetas_dot)

tau = 20  # bounds on torque

# EPSILON_THETAS = 1
# EPSILON_DOTS = 0.5

lower_bounds = [-EPSILON_THETAS + pi, -EPSILON_THETAS, -EPSILON_DOTS, -EPSILON_DOTS]
upper_bounds = [EPSILON_THETAS + pi, EPSILON_THETAS, EPSILON_DOTS, EPSILON_DOTS]

# base name for the output files.
base_name = "Acrobot_step" + str(STEP) + "_torque" + str(tau) + \
    "_" + str(subdiv_init) + "_" + str(int(100*EPSILON_THETAS))

print(base_name)

# # plot
# fig, ax = RoA.PlotMorseTiles(lower_bounds, upper_bounds, from_file=base_name)
#
# plt.savefig(base_name)
# plt.show()


# fig, ax = RoA.PlotMorseTiles(lower_bounds, upper_bounds,
#                              from_file=base_name, from_file_basic=True)
#
# plt.savefig(base_name)
# plt.show()


# plot

# for i in np.linspace(-0.5, 0.5, 3):
#     for j in np.linspace(-0.5, 0.5, 3):
#
#         section = ([2, 3], (0, 0, i, j))
#         name_plot = base_name + "RoA" + str(section)
#         fig, ax = RoA.PlotTiles(lower_bounds, upper_bounds,
#                                 from_file=base_name,  section=section, name_plot=name_plot, from_file_basic=True)


section = ([2, 3], (0, 0, 0, 0))
name_plot = base_name + "RoA" + str(section)
fig, ax = RoA.PlotTiles(lower_bounds, upper_bounds,
                        from_file=base_name,  section=section, name_plot=name_plot, from_file_basic=False)

plt.show()

# proj_dims = [1, 2]
# name_plot = base_name + "RoA" + str(proj_dims)
# DG.PlotOrderRetraction(morse_graph, map_graph, retract_tiles,
#                        retract_indices, proj_dims=proj_dims, name_plot=name_plot)
#
# proj_dims = [0, 2]
# name_plot = base_name + "RoA" + str(proj_dims)
# DG.PlotOrderRetraction(morse_graph, map_graph, retract_tiles,
#                        retract_indices, proj_dims=proj_dims, name_plot=name_plot)
