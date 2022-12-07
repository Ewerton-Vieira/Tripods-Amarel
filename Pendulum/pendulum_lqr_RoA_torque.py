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


sb = 1
time = 1  # time is equal to 10s

# subdiv_min = 10  # minimal subdivision to compute Morse Graph
# subdiv_max = 10  # maximal subdivision to compute Morse Graph
subdiv_init = subdiv_min = subdiv_max = sb  # non adaptive proceedure


x_min = -3.14159
x_max = 3.14159

y_min = -6.28318
y_max = 6.28318

torque = 0.736

# base name for the output files.
base_name = "pendulum_lqr_time" + \
    str(time) + "_" + \
    str(subdiv_init) + str(int(1000*torque))


print(base_name)


# Define the parameters for CMGDB
lower_bounds = [x_min, y_min]
upper_bounds = [x_max, y_max]


# load map
# set the time step
TM = TimeMap.TimeMap("pendulum_lc", time,
                     "examples/tripods/lc_roa.yaml")
# define the lqr time map for the pendulum

TM1 = TimeMap.TimeMap("pendulum_lc", 0.01,
                      "examples/tripods/lc_roa.yaml")


TM.cs.set_bounds([-1*torque], [torque])
TM1.cs.set_bounds([-1*torque], [torque])


def g(X):
    Y = TM.pendulum_lqr(X)
    return Y


phase_periodic = [True, False]


def F(rect):
    return CMGDB.BoxMap(g, rect, padding=True)
    # return MG_util.F_K(g, rect, K)
    # return MG_util.BoxMapK(g_on_grid, rect, K)


morse_graph, map_graph = MG_util.run_CMGDB(
    subdiv_min, subdiv_max, lower_bounds, upper_bounds, phase_periodic, F, base_name, subdiv_init)

# CMGDB.PlotMorseSets(morse_graph)

startTime = datetime.now()

roa = RoA.RoA(map_graph, morse_graph)

print(f"Time to build the regions of attraction = {datetime.now() - startTime}")

roa.save_file(base_name)

# fig, ax = roa.PlotTiles()
#
# fig, ax = dyn_tools.Plot_trajectories(lower_bounds, upper_bounds, TM1.pendulum_lqr, fig=fig, ax=ax, xlim=[
#                                       lower_bounds[0], upper_bounds[0]], ylim=[lower_bounds[1], upper_bounds[1]])


fig, ax = dyn_tools.Plot_trajectories(lower_bounds, upper_bounds, TM1.pendulum_lqr, xlim=[
                                      lower_bounds[0], upper_bounds[0]], ylim=[lower_bounds[1], upper_bounds[1]])


def d_dt(x, t):
    y = TM1.pendulum_lqr(x)
    norm = np.sqrt((y[0]-x[0]) ** 2 + (y[1]-x[1]) ** 2)
    return [(y[0]-x[0])/norm, (y[1]-x[1])/norm]


fig, ax = dyn_tools.Plot_vectors(lower_bounds, upper_bounds, d_dt, fig=fig, ax=ax, xlim=[
    lower_bounds[0], upper_bounds[0]], ylim=[lower_bounds[1], upper_bounds[1]])


ax.set_xlabel(r"$\theta$")
ax.set_ylabel(r"$\dot\theta$")
plt.savefig(base_name, bbox_inches='tight')
plt.show()
