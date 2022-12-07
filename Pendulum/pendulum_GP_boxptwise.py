# ---------------- import packages ----------------
import GP_function
import csv
from datetime import datetime
import matplotlib
import matplotlib.pyplot as plt
import random
import pandas as pd
import numpy as np
import dyn_tools
import RoA
import TimeMap
import MultivaluedMap
import CMGDB
import CMGDB_util
import libpyDirtMP as prx
import sys
import os
import warnings
warnings.filterwarnings("ignore")


def pplot(x_add, y_add, base_name="out"):

    fig_w = 8
    fig_h = 8
    fig1, ax1 = plt.subplots(figsize=(fig_w, fig_h))

    COLOR_X = 'ro'

    COLOR_Y = 'bx'
    LABEL_X = 'Initial points'
    LABEL_Y = 'Endpoints'

    ax1.plot(x_add[:, 0], x_add[:, 1], COLOR_X, label=LABEL_X)
    ax1.plot(y_add[:, 0], y_add[:, 1], COLOR_Y, label=LABEL_Y)

    tick = 5  # tick for 2D plots
    d1 = 0
    d2 = 1

    fontsize = 32

    plt.xticks(np.linspace(lower_bounds[d1], upper_bounds[d1], tick))
    plt.yticks(np.linspace(lower_bounds[d2], upper_bounds[d2], tick))

    ax1.set_xlabel(r"$\theta$")
    ax1.set_ylabel(r"$\dot \theta$")
    plt.xticks(fontsize=fontsize)
    plt.yticks(fontsize=fontsize)
    ax1.xaxis.label.set_size(fontsize)
    ax1.yaxis.label.set_size(fontsize)

    plt.savefig(outpath + base_name + "_data_" + str(len(x_add)) + ".png", bbox_inches='tight')
    plt.show()


def choose_point(add, seed, boxes):
    np.random.seed(seed)
    random.shuffle(boxes)
    xnew = np.zeros((1, 2))
    ynew = np.zeros((1, 2))

    count = 0
    i = 0
    while count + i//8 < add:
        if i >= len(boxes):
            xnew = np.append(xnew, MG_util.sample_points(lower_bounds, upper_bounds, 1), axis=0)
        else:
            xmin, ymin, xmax, ymax = morse_graph.phase_space_box(boxes[i])
            if (((xmin > -1) & (ymin < 0)) or ((xmin < -1) & (ymin > 0)) or ((xmin > 1) & (ymin < 0)) or ((xmin < 1) & (ymin > 0))):
                xnew = np.append(xnew, MG_util.sample_points([xmin, ymin], [xmax, ymax], 1), axis=0)
                count += 1
        i += 1
    ynew = np.array([g(i) for i in xnew[1:, ]])
    return xnew[1:, ], ynew


# ---------------- set dynamic system setting ----------------
MG_util = CMGDB_util.CMGDB_util()

outpath = os.path.abspath(os.getcwd()) + "/output/"

sb = 12
subdiv_init = subdiv_min = subdiv_max = sb  # non adaptive proceedure

# phase_periodic = [True, False]
#
# x_min = -3.14159
# x_max = 3.14159
#
# y_min = -6.28318
# y_max = 6.28318

phase_periodic = [False, False]

x_min = -3.14
x_max = 3.14

y_min = -6.28
y_max = 6.28

# Define the parameters for CMGDB
lower_bounds = [x_min, y_min]
upper_bounds = [x_max, y_max]

time = 1

TM = TimeMap.TimeMap("pendulum_lc", time,
                     "examples/tripods/pendulum_lc.yaml")


def g(X):
    # Y = TM.pendulum_lc(X) # Pendulum + LC
    Y = TM.pendulum_lqr(X)  # Pendulum + LQR
    return Y


# ---------------- random sampling & build GP ----------------
# ------------ initial points ------------
np.random.seed(324)  # specify a seed to generate points #

n = 300  # specify a number of initial points #

# generate training data
X = MG_util.sample_points(lower_bounds, upper_bounds, n)
Y = [g(x_) for x_ in X]
Y = np.array(Y)

# base name for the output files
base_name = "pendulum_lqr_time" + \
    str(time) + "_" + \
    str(subdiv_init) + "_" + \
    "box_ptwise" + "_" + str(n) + "_0"

pplot(X, Y, base_name=base_name)

# build GP models
GP = GP_function.GP(X, Y)
GP.skl_fit()

# plt.show()


# Y_out = [GP.skl_learned_f(x_)[0][0] for x_ in X]
# Y_out = np.array(Y_out)
# plt.scatter(X[:, 0], X[:, 1])
# plt.scatter(Y_out[:, 0], Y_out[:, 1])
# plt.show()


def F(rect):
    # return MG_util.Box_ptwise(GP.skl_learned_f, rect, n=-3)
    return MG_util.Box_GP_K(GP.skl_learned_f, rect, K=0.5, n=-3)


morse_graph, map_graph = MG_util.run_CMGDB(
    subdiv_min, subdiv_max, lower_bounds, upper_bounds, phase_periodic, F, base_name, subdiv_init)

# CMGDB.PlotMorseSets(morse_graph)

roa = RoA.RoA(map_graph, morse_graph)

# roa.save_file(base_name)

name_plot = base_name + "_RoA"
fig, ax = roa.PlotTiles()
ax.set_xlabel(r"$\theta$")
ax.set_ylabel(r"$\dot \theta$")
plt.show()

# plt.savefig(outpath + base_name + ".png", bbox_inches='tight')
# plt.show()

# grid_x = np.linspace(lower_bounds[0], upper_bounds[0], 100)
# grid_y = np.linspace(lower_bounds[1], upper_bounds[1], 100)
# grid_X, grid_Y = np.meshgrid(grid_x, grid_y)
#
# grid_Z = GP.z_std(grid_X, grid_Y)
#
# fig1, ax2 = plt.subplots(constrained_layout=True)
#
# CS = ax2.contourf(grid_X, grid_Y, grid_Z, 20, cmap='RdGy')
# ax2.contour(CS, levels=CS.levels[::2], colors='r')
# # plt.colorbar()
# plt.savefig(outpath + base_name + "_std.png")
# plt.show()


nt = roa.assign_morse_nodes2tiles()
retract_tiles, retract_indices = retract_tiles, retract_indices = list(nt.values()), list(nt.keys())
Vol = roa.Morse_sets_vol()
idx = [k for k in Vol if Vol[k] < 10]
boxes1 = [retract_indices[i] for i in range(len(retract_tiles)) if retract_tiles[i] in idx]
boxes2 = [retract_indices[i] for i in range(len(retract_tiles)) if(
    retract_tiles[i] == retract_tiles[retract_indices.index(1706)])]

add = 300
x1, y1 = choose_point(add, 453, boxes1)
x2, y2 = choose_point(add, 786, boxes2)

x_add = X.copy()
y_add = Y.copy()

x_add = np.append(x_add, np.append(x1, x2, axis=0), axis=0)
y_add = np.append(y_add, np.append(y1, y2, axis=0), axis=0)

pplot(x_add, y_add, base_name=base_name)

#
# # ------------ adaptive points 20 steps ------------
#
# x_add = X.copy()
# y_add = Y.copy()
#
# for i in range(20):
#     startTime = datetime.now()
#
#     x_add = np.append(x_add, np.append(x1, x2, axis=0), axis=0)
#     y_add = np.append(y_add, np.append(y1, y2, axis=0), axis=0)
#
#     GP = GP_function.GP(x_add, y_add)
#     GP.skl_fit()
#
#     base_name = "pendulum_lqr_time" + \
#         str(time) + "_" + \
#         str(subdiv_init) + "_" + \
#         "box_ptwise" + "_" + str(n) + "_" + str(i+1)
#
#     morse_graph, map_graph = MG_util.run_CMGDB(
#         subdiv_min, subdiv_max, lower_bounds, upper_bounds, phase_periodic, F, base_name, subdiv_init)
#
#     roa = RoA.RoA(map_graph, morse_graph)
#
#     nt = roa.assign_morse_nodes2tiles()
#     retract_tiles, retract_indices = retract_tiles, retract_indices = list(
#         nt.values()), list(nt.keys())
#     Vol = roa.Morse_sets_vol()
#     idx = [k for k in Vol if Vol[k] < 10]
#     boxes1 = [retract_indices[i] for i in range(len(retract_tiles)) if retract_tiles[i] in idx]
#     boxes2 = [retract_indices[i] for i in range(len(retract_tiles)) if(
#         retract_tiles[i] == retract_tiles[retract_indices.index(1706)])]
#     x1, y1 = choose_point(add, 123*i, boxes1)
#     x2, y2 = choose_point(add, 321*i, boxes2)
#
#     fig, ax = roa.PlotTiles()
#     ax.set_xlabel(r"$\theta$")
#     ax.set_ylabel(r"$\dot \theta$")
#
#     plt.savefig(outpath + base_name + ".png", bbox_inches='tight')
#

"""

add = 5
x1, y1 = choose_point(add, 123, boxes1)
x2, y2 = choose_point(add, 321, boxes2)

# ------------ adaptive points 30 ------------

x_add = X.copy()
y_add = Y.copy()

for i in range(30):
    startTime = datetime.now()

    x_add = np.append(x_add, np.append(x1, x2, axis=0), axis=0)
    y_add = np.append(y_add, np.append(y1, y2, axis=0), axis=0)

    GP = GP_function.GP(x_add, y_add)
    GP.skl_fit()

    base_name = "pendulum_lqr_time" + \
        str(time) + "_" + \
        str(subdiv_init) + "_" + \
        "box_ptwise" + "_" + str(n) + "_" + str(i+1)

    morse_graph, map_graph = MG_util.run_CMGDB(
        subdiv_min, subdiv_max, lower_bounds, upper_bounds, phase_periodic, F, base_name, subdiv_init)

    roa = RoA.RoA(map_graph, morse_graph)

    nt = roa.assign_morse_nodes2tiles()
    retract_tiles, retract_indices = retract_tiles, retract_indices = list(
        nt.values()), list(nt.keys())
    Vol = roa.Morse_sets_vol()
    idx = [k for k in Vol if Vol[k] < 10]
    boxes1 = [retract_indices[i] for i in range(len(retract_tiles)) if retract_tiles[i] in idx]
    boxes2 = [retract_indices[i] for i in range(len(retract_tiles)) if(
        retract_tiles[i] == retract_tiles[retract_indices.index(1706)])]
    x1, y1 = choose_point(add, 123*i, boxes1)
    x2, y2 = choose_point(add, 321*i, boxes2)

fig, ax = roa.PlotTiles()
ax.set_xlabel(r"$\theta$")
ax.set_ylabel(r"$\dot \theta$")

plt.savefig(outpath + base_name + ".png", bbox_inches='tight')

# ------------ adaptive points 60 ------------


def F(rect):
    return MG_util.Box_ptwise(GP.skl_learned_f, rect, n=-2)


for i in range(30, 60):
    startTime = datetime.now()

    x_add = np.append(x_add, np.append(x1, x2, axis=0), axis=0)
    y_add = np.append(y_add, np.append(y1, y2, axis=0), axis=0)

    GP = GP_function.GP(x_add, y_add)
    GP.skl_fit()

    base_name = "pendulum_lqr_time" + \
        str(time) + "_" + \
        str(subdiv_init) + "_" + \
        "box_ptwise" + "_" + str(n) + "_" + str(i+1)

    morse_graph, map_graph = MG_util.run_CMGDB(
        subdiv_min, subdiv_max, lower_bounds, upper_bounds, phase_periodic, F, base_name, subdiv_init)

    roa = RoA.RoA(map_graph, morse_graph)

    nt = roa.assign_morse_nodes2tiles()
    retract_tiles, retract_indices = retract_tiles, retract_indices = list(
        nt.values()), list(nt.keys())
    Vol = roa.Morse_sets_vol()
    idx = [k for k in Vol if Vol[k] < 10]
    boxes1 = [retract_indices[i] for i in range(len(retract_tiles)) if retract_tiles[i] in idx]
    boxes2 = [retract_indices[i] for i in range(len(retract_tiles)) if(
        retract_tiles[i] == retract_tiles[retract_indices.index(1706)])]
    x1, y1 = choose_point(add, 123*i, boxes1)
    x2, y2 = choose_point(add, 321*i, boxes2)

fig, ax = roa.PlotTiles()
ax.set_xlabel(r"$\theta$")
ax.set_ylabel(r"$\dot \theta$")

plt.savefig(outpath + base_name + ".png", bbox_inches='tight')
# ------------ adaptive points 90 ------------


def F(rect):
    return MG_util.Box_ptwise(GP.skl_learned_f, rect, n=-2)


for i in range(60, 90):
    x_add = np.append(x_add, np.append(x1, x2, axis=0), axis=0)
    y_add = np.append(y_add, np.append(y1, y2, axis=0), axis=0)

    GP = GP_function.GP(x_add, y_add)
    GP.skl_fit()

    base_name = "pendulum_lqr_time" + \
        str(time) + "_" + \
        str(subdiv_init) + "_" + \
        "box_ptwise" + "_" + str(n) + "_" + str(i+1)

    morse_graph, map_graph = MG_util.run_CMGDB(
        subdiv_min, subdiv_max, lower_bounds, upper_bounds, phase_periodic, F, base_name, subdiv_init)

    roa = RoA.RoA(map_graph, morse_graph)

    fig, ax = roa.PlotTiles()

    nt = roa.assign_morse_nodes2tiles()
    retract_tiles, retract_indices = retract_tiles, retract_indices = list(
        nt.values()), list(nt.keys())
    Vol = roa.Morse_sets_vol()
    boxes1 = [retract_indices[i] for i in range(
        len(retract_tiles)) if retract_tiles[i] != retract_tiles[retract_indices.index(1706)]]
    boxes2 = [retract_indices[i] for i in range(
        len(retract_tiles)) if retract_tiles[i] == retract_tiles[retract_indices.index(1706)]]
    x1, y1 = choose_point(add, 123*i, boxes1)
    x2, y2 = choose_point(add, 321*i, boxes2)

roa.save_file(base_name)

name_plot = base_name + "_RoA"
fig, ax = roa.PlotTiles()
ax.set_xlabel(r"$\theta$")
ax.set_ylabel(r"$\dot \theta$")

plt.savefig(outpath + base_name + ".png", bbox_inches='tight')

grid_Z = GP.z_std(grid_X, grid_Y)
plt.contourf(grid_X, grid_Y, grid_Z, 20, cmap='RdGy')
plt.colorbar()
plt.savefig(outpath + base_name + "_std.png")
"""
