import CMGDB_util
import CMGDB
import RoA
import sys

import NoisyTimeMap

import numpy as np

import matplotlib.pyplot as plt

from datetime import datetime

MG_util = CMGDB_util.CMGDB_util()


sb = 20
time = 1  # time is equal to 10s

# subdiv_min = 10  # minimal subdivision to compute Morse Graph
# subdiv_max = 10  # maximal subdivision to compute Morse Graph
subdiv_init = subdiv_min = subdiv_max = sb  # non adaptive proceedure


# base name for the output files.
base_name = "Lander_time" + \
    str(time) + "_" + \
    str(subdiv_init)


print(base_name)


# load map
# set the time step
TM = NoisyTimeMap.NoisyTimeMap("examples/tripods/lander_roa.yaml")

TM.duration = time
# define the lqr time map for the pendulum

# Define the parameters for CMGDB
lower_bounds = TM.ss.get_lower_bounds()
upper_bounds = TM.ss.get_upper_bounds()
lower_bounds[0] = 0
print(lower_bounds, upper_bounds)

"""
def g(X):
    # Y = TM.lander_analytical(X)
    # if -0.2 <= Y[0] <= 0.1 and Y[1] < - 0.1:
    #     Y[0] = -1
    # return Y
    return TM.lander_analytical(X)


phase_periodic = [False, False, False]


def F(rect):
    # return CMGDB.BoxMap(g, rect, padding=False)
    return MG_util.BoxMapK(g, rect, K=[0.1, 0.1, 0.1])
    # return MG_util.Box_noisy_K(g, rect, K, noise)


morse_graph, map_graph = MG_util.run_CMGDB(
    subdiv_min, subdiv_max, lower_bounds, upper_bounds, phase_periodic, F, base_name, subdiv_init)

# CMGDB.PlotMorseSets(morse_graph)

startTime = datetime.now()

roa = RoA.RoA(map_graph, morse_graph)

print(f"Time to build the regions of attraction = {datetime.now() - startTime}")

roa.save_file(base_name)

# fig, ax = roa.PlotTiles()


# # cubes
# name_plot = base_name + "RoA"
# fig, ax = roa.PlotTiles(lower_bounds, upper_bounds,
#                         from_file=base_name, name_plot=name_plot)
#


# points
name_plot = base_name + "RoA"
fig, ax = RoA.PlotTiles(lower_bounds, upper_bounds,
                        from_file=base_name, name_plot=name_plot, plot_point=True)

#
# section = ([2], (0, 0, 2134))
# name_plot = base_name + "RoA"
# fig, ax = roa.PlotTiles(lower_bounds, upper_bounds,
#                         from_file=base_name,  section=section, name_plot=name_plot)


ax.set_xlabel(r"$h$")
ax.set_ylabel(r"$\dot h$")
ax.set_zlabel(r'$m$')
plt.savefig(base_name, bbox_inches='tight')
plt.show()
"""
