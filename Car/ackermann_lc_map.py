
import numpy as np
from datetime import datetime

import Grid
import Ackermann
import TimeMap


sb = 7
time = 10  # time in seconds

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

lower_bounds = [x_min, y_min, -THETA_BOUND]
upper_bounds = [x_max, y_max, THETA_BOUND]

# base name for the output files.
# base name for the output files.
base_name = f"learned_ack_time{time}_{subdiv_init}_map_grid"

print(base_name)


# ### Loading functions


def g(X):
    return TM.ackermann_lc(X)


# Grid
grid = Grid.Grid(lower_bounds, upper_bounds, sb, base_name=base_name)

startTime = datetime.now()
grid.write_map_grid(g, lower_bounds, upper_bounds, sb, base_name=base_name)
print(f"Time to save map_grid = {datetime.now() - startTime}")
#
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
# vertex = [(upper_bounds[a] - lower_bounds[a])/(2**(1 + (a & 1))) for a in range(len(upper_bounds))]
#
# print("region, vertex coordinates", grid.vertex2grid_vertex(
#     vertex, lower_bounds, upper_bounds, sb))
# print("g image ", g(vertex))
# print(g(vertex))
# print(g_on_grid(vertex))
