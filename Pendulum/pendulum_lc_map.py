import numpy as np
from datetime import datetime

import Grid
import TimeMap


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
base_name = f"learned_pendulum_time{time}_{subdiv_init}_map_grid"


print(base_name)


# ### Loading functions


def g(X):
    return TM.pendulum_lc(X)


# Define the parameters for CMGDB
lower_bounds = [x_min, y_min]
upper_bounds = [x_max, y_max]

# Grid
grid = Grid.Grid(lower_bounds, upper_bounds, sb, base_name=base_name)

grid.write_map_grid(g, lower_bounds, upper_bounds, sb, base_name=base_name)

# # load map
# file_name = base_name + ".csv"
# map = grid.load_map_grid(file_name, lower_bounds, upper_bounds, sb)
#
#
# def g_on_grid(x):
#     return grid.image_of_vertex_from_loaded_map(map, x, lower_bounds, upper_bounds, sb)
#
#
# # test
# vertex = [(x_max - x_min)/(2**2), (y_max - y_min)/2**2]
# # vertex = [x_min, y_max]
# print("region, vertex coordinates", grid.vertex2grid_vertex(
#     vertex, lower_bounds, upper_bounds, sb))
# print("g image ", g(vertex))
# print(g(vertex))
# print(g_on_grid(vertex))
