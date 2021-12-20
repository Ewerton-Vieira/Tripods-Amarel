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


STEP = 9  # step is equal to STEP * 0.1s

TM = TimeMap.TimeMap("pendulum_lc", STEP,
                     "examples/tripods/lc_roa.yaml")

# subdiv_min = 10  # minimal subdivision to compute Morse Graph
# subdiv_max = 10  # maximal subdivision to compute Morse Graph
subdiv_init = subdiv_min = subdiv_max = 14  # non adaptive proceedure


x_min = -3.14159
x_max = 3.14159

y_min = -6.28318
y_max = 6.28318


# x_min = -1
# x_max = 1
# y_min = -1
# y_max = 1


# base name for the output files.
base_name = "learned_pendulum_step" + \
    str(STEP) + "_" + \
    str(subdiv_init)


print(base_name)


# ### Loading functions


def g(X):
    return TM.pendulum_lc(X)


print(g([0.6, 0.6]))


# Define the parameters for CMGDB
lower_bounds = [x_min, y_min]
upper_bounds = [x_max, y_max]

phase_periodic = [True, False]

# K = sampled_Lipschitz(lower_bounds, upper_bounds, N, g, base_name)
K = [1.1, 1.1]


def F(rect):
    return CMGDB.BoxMap(g, rect, padding=True)
    # return MG_util.F_K(rect, g, K)


morse_graph, map_graph = MG_util.run_CMGDB(
    subdiv_min, subdiv_max, lower_bounds, upper_bounds, phase_periodic, F, base_name, subdiv_init)

startTime = datetime.now()

DG = ROA.Domain_Graph(map_graph, morse_graph)

print(f"Time to build the ancestors_graph time = {datetime.now() - startTime}")

retract_tiles, retract_indices, morse_nodes_map = DG.morse_retract()

DG.save_file(retract_tiles, retract_indices, base_name)

TM1 = TimeMap.TimeMap("pendulum_lc", 0.01,
                      "examples/tripods/lc_roa.yaml")


def d_dt(X, t):
    X_f = TM1.pendulum_lc(X)
    return [X_f[0] - X[0], X_f[1] - X[1]]


fig, ax = ROA.PlotMorseTiles(lower_bounds, upper_bounds, from_file=base_name)
#
# fig, ax = dyn_tools.Plot_vectors(lower_bounds, upper_bounds, d_dt, fig=fig, ax=ax, normalize=False)


# fig, ax = dyn_tools.Plot_vectors(lower_bounds, upper_bounds, d_dt, normalize=False)


# ROA.PlotMorseTiles(lower_bounds, upper_bounds, from_file=base_name)

# def phi(X):
#     return Pd.G_traj(X, STEP//10)
#
#
# fig, ax = dyn_tools.Plot_trajectories(
#     lower_bounds, upper_bounds, phi, fig=None, ax=None, normalize=False)


fig, ax = dyn_tools.Plot_trajectories(lower_bounds, upper_bounds, TM1.pendulum_lc, fig=fig, ax=ax, xlim=[
                                      lower_bounds[0], upper_bounds[0]], ylim=[lower_bounds[1], upper_bounds[1]])

plt.savefig(base_name)
plt.show()
