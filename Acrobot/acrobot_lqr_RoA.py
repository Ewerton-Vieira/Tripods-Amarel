import CMGDB_util
import CMGDB
import RoA
import dyn_tools
import Grid
from Acrobot import *


import numpy as np

import matplotlib.pyplot as plt

from datetime import datetime


sb = 25
time = 5  # time in seconds
STEP = 500

MG_util = CMGDB_util.CMGDB_util()

subdiv_init = subdiv_min = subdiv_max = sb  # non adaptive proceedure

# POSITION_BOUNDS
EPSILON_THETAS = pi = 3.141592653589793  # size of the box with the center at the goal (thetas)
EPSILON_DOTS = 6  # 6  # size of the box with the center at the goal (thetas_dot)

tau = 14  # bounds on torque


lower_bounds = [-EPSILON_THETAS + pi, -EPSILON_THETAS, -EPSILON_DOTS, -EPSILON_DOTS]
upper_bounds = [EPSILON_THETAS + pi, EPSILON_THETAS, EPSILON_DOTS, EPSILON_DOTS]

# base name for the output files.
base_name = "Acrobot_step" + str(STEP) + "_torque" + str(tau) + "_" + str(subdiv_init)

print(base_name)


def g(X):
    return G(X, tau, STEP)


phase_periodic = [True, True, False, False]

K = 2
K = [K, K, K]


def F(rect):
    return CMGDB.BoxMap(g, rect, padding=True)
    # return MG_util.F_K(g_on_grid, rect, K)
    # return MG_util.BoxMapK(g_on_grid, rect, K)


morse_graph, map_graph = MG_util.run_CMGDB(
    subdiv_min, subdiv_max, lower_bounds, upper_bounds, phase_periodic, F, base_name, subdiv_init)

startTime = datetime.now()

roa = RoA.RoA(map_graph, morse_graph)

print(f"Time to build the regions of attraction = {datetime.now() - startTime}")

roa.save_file(base_name)
