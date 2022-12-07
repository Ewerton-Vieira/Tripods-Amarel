import CMGDB_util
import CMGDB
import RoA
import dyn_tools
import sys

import TimeMap

import numpy as np

import matplotlib.pyplot as plt

from datetime import datetime

MG_util = CMGDB_util.CMGDB_util()


sb = 18
time = 10  # time is equal to time * 0.1s

# subdiv_min = 10  # minimal subdivision to compute Morse Graph
# subdiv_max = 10  # maximal subdivision to compute Morse Graph
subdiv_init = subdiv_min = subdiv_max = sb  # non adaptive proceedure


# base name for the output files.
base_name = f"Ack_lc_obs_{time}_{subdiv_init}"


print(base_name)

# load map
# set the time step
TM = TimeMap.TimeMap("ackermann_lc", time,
                     "examples/tripods/ackermann_lc.yaml")

# Define the parameters for CMGDB
TM.ss.print_bounds()
lower_bounds = TM.ss.get_lower_bounds()
upper_bounds = TM.ss.get_upper_bounds()

lower_bounds = [-10, -10, -3.141592653589793]
upper_bounds = [10, 10, 3.141592653589793]

print(lower_bounds, upper_bounds)


def g(X):
    return TM.ackermann_lc(X)[0]


print(g([9.1, -0.8, 0]))

phase_periodic = [False, False, True]


def F(rect):
    return CMGDB.BoxMap(g, rect, padding=False)


morse_graph, map_graph = MG_util.run_CMGDB(
    subdiv_min, subdiv_max, lower_bounds, upper_bounds, phase_periodic, F, base_name, subdiv_init)

# CMGDB.PlotMorseSets(morse_graph)

startTime = datetime.now()

roa = RoA.RoA(map_graph, morse_graph)

print(f"Time to build the regions of attraction = {datetime.now() - startTime}")

roa.save_file(base_name)

# fig, ax = roa.PlotTiles()

# points
name_plot = base_name + "RoA"
fig, ax = RoA.PlotTiles(lower_bounds, upper_bounds,
                        from_file=base_name, name_plot=name_plot, plot_point=True)


# section = ([2], (0, 0, 1.57))
# name_plot = base_name + "RoA"
# fig, ax = RoA.PlotTiles(lower_bounds, upper_bounds,
#                         from_file=base_name,  section=section, name_plot=name_plot)

ax.set_xlabel(r"$x$")
ax.set_ylabel(r"$y$")
ax.set_zlabel(r'$\theta$')
plt.savefig(base_name, bbox_inches='tight')
plt.show()
