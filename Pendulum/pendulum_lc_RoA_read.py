# import Pendulum_lc as Pd

import CMGDB_util
import CMGDB
import RoA
import dyn_tools
import Grid
import sys

import TimeMap

import numpy as np

import matplotlib

import matplotlib.pyplot as plt

from datetime import datetime


MG_util = CMGDB_util.CMGDB_util()


sb = 12
time = 1  # time is equal to 10s

# TM = TimeMap.TimeMap("pendulum_lc", time,
#                      "examples/tripods/lc_roa.yaml")

# subdiv_min = 10  # minimal subdivision to compute Morse Graph
# subdiv_max = 10  # maximal subdivision to compute Morse Graph
subdiv_init = subdiv_min = subdiv_max = sb  # non adaptive proceedure


x_min = -3.14159
x_max = 3.14159

y_min = -6.28318
y_max = 6.28318


# base name for the output files.


base_name = "pendulum_lc_time" + \
    str(time) + "_" + \
    str(subdiv_init)

base_name = "pendulum_lqr_time" + \
    str(time) + "_" + \
    str(subdiv_init)

print(base_name)

# Define the parameters for CMGDB
lower_bounds = [x_min, y_min]
upper_bounds = [x_max, y_max]


# fig, ax = RoA.PlotTiles(lower_bounds, upper_bounds, selection=[4], from_file=base_name)

# fig, ax = RoA.PlotTiles(lower_bounds, upper_bounds, cmap=matplotlib.cm.hsv,
#                         selection=[0], from_file=base_name)


viridis = matplotlib.cm.get_cmap('viridis', 256)
newcolors = viridis(np.linspace(0, 1, 256))
orange = np.array([253/256, 174/256, 97/256, 1])
yellowish = np.array([233/256, 204/256, 50/256, 1])
newcolors[109:146, :] = orange
newcolors[219:, :] = yellowish
newcmp = matplotlib.colors.ListedColormap(newcolors)


fig, ax = RoA.PlotTiles(lower_bounds, upper_bounds, cmap=newcmp,
                        from_file=base_name, fig_w=16, fig_h=16)


# dynamics
#
TM1 = TimeMap.TimeMap("pendulum_lc", 0.01,
                      "examples/tripods/lc_roa.yaml")

# fig, ax = dyn_tools.Plot_trajectories(lower_bounds, upper_bounds, TM1.pendulum_lc, fig=fig, ax=ax, xlim=[
#                                       lower_bounds[0], upper_bounds[0]], ylim=[lower_bounds[1], upper_bounds[1]])
#
fig, ax = dyn_tools.Plot_trajectories(lower_bounds, upper_bounds, TM1.pendulum_lqr, fig=fig, ax=ax, xlim=[
                                      lower_bounds[0], upper_bounds[0]], ylim=[lower_bounds[1], upper_bounds[1]])

ax.set_xlabel(r"$\theta$")
ax.set_ylabel(r"$\dot\theta$")
plt.savefig(base_name, bbox_inches='tight')
plt.show()


# A = {11: 0.7674471902831467, 0: 3.187857559637488, 2: 16.616376214104925, 3: 14.10199271940891, 1: 18.400660811924254, 9: 1.772236761234638, 4: 14.13693144549715, 5: 0.38191641965424983, 12: 0.5481765644879616, 13: 4.609502276331415, 6: 0.9951513016858389, 7: 2.790278952426475, 8: 0.21083714018767685, 10: 0.16866971215014126}
#
# print(sum([A[i] for i in {0,1,2,3,6,7,8,9,10,11,13}]))
#
# print(sum([A[i] for i in {4}]))
#
# print(sum([A[i] for i in {5,12}]))
