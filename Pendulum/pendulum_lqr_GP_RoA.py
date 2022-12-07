import CMGDB_util
import CMGDB
import RoA
import dyn_tools
import Grid
import sys
import GPy

import TimeMap

import numpy as np

import matplotlib.pyplot as plt
import matplotlib

from datetime import datetime


# friendly colors
viridis = matplotlib.cm.get_cmap('viridis', 256)
newcolors = viridis(np.linspace(0, 1, 256))
orange = np.array([253/256, 174/256, 97/256, 1])
yellowish = np.array([233/256, 204/256, 50/256, 1])
newcolors[109:146, :] = orange
newcolors[219:, :] = yellowish
newcmp = matplotlib.colors.ListedColormap(newcolors)
####

MG_util = CMGDB_util.CMGDB_util()


sb = 12
time = 1  # time is equal to 10s

# subdiv_min = 10  # minimal subdivision to compute Morse Graph
# subdiv_max = 10  # maximal subdivision to compute Morse Graph
subdiv_init = subdiv_min = subdiv_max = sb  # non adaptive proceedure


x_min = -3.14159
x_max = 3.14159

y_min = -6.28318
y_max = 6.28318


# base name for the output files.
base_name = "pendulum_lqr_GP_time" + \
    str(time) + "_" + \
    str(subdiv_init)


print(base_name)


# Define the parameters for CMGDB
lower_bounds = [x_min, y_min]
upper_bounds = [x_max, y_max]


# load map
# set the time step
TM = TimeMap.TimeMap("pendulum_lc", time,
                     "examples/tripods/pendulum_lc.yaml")

# define the lqr time map for the pendulum


def g(X):
    return TM.pendulum_lqr(X)


phase_periodic = [True, False]

#### GP ###


def sample_points(lower_bounds, upper_bounds, num_pts):
    # Sample num_pts in dimension dim, where each
    # component of the sampled points are in the
    # ranges given by lower_bounds and upper_bounds
    dim = len(lower_bounds)
    X = np.random.uniform(lower_bounds, upper_bounds, size=(num_pts, dim))
    return X


np.random.seed(123)  # specify a seed to generate points #

n = 600  # specify a number of initial points #

# generate training data
X = sample_points(lower_bounds, upper_bounds, n)
Y = [g(x_) for x_ in X]
Y = np.array(Y)

Y.shape


# define kernels
kern1 = GPy.kern.RBF(input_dim=2, ARD=True)
gp1 = GPy.models.GPRegression(X, Y[:, 0].reshape(-1, 1), kern1)
# interpolation
gp1.likelihood.variance.fix(1e-5)
gp1.optimize()

kern2 = GPy.kern.RBF(input_dim=2, ARD=True)
gp2 = GPy.models.GPRegression(X, Y[:, 1].reshape(-1, 1), kern2)
# interpolation
gp2.likelihood.variance.fix(1e-5)
gp2.optimize()

# prediction function


def learned_f(X):
    X = np.array(X).reshape(1, -1)
    y1, s1 = gp1.predict(X)
    y2, s2 = gp2.predict(X)
    return np.concatenate((y1, y2), axis=1), np.concatenate((s1, s2), axis=0).reshape(1, -1)


def mean(X):
    return learned_f(X)[0][0]


learned_f([1, 1])
mean([1, 1])
####

gp1.predictive_gradients(np.array([1, 1]).reshape(-1, 2))
gp2.predictive_gradients(np.array([1, 1]).reshape(-1, 2))


def J(X):
    grad_1, s1 = gp1.predictive_gradients(np.array(X).reshape(-1, 2))
    grad_2, s2 = gp2.predictive_gradients(np.array(X).reshape(-1, 2))
    return np.concatenate((grad_1[0].T, grad_2[0].T), axis=0), np.concatenate((s1, s2), axis=1)


J([1, 1])


def K(X):
    k = 2
    return k * np.ones((2, 2)), np.zeros((2, 2))


def F(rect):
    # return CMGDB.BoxMap(mean, rect, padding=True)

    # return MG_util.BoxMapK(mean, rect, K=2)

    # return MG_util.Box_ptwise(learned_f, rect, n=-2)

    return MG_util.F_J(learned_f, J, rect, lower_bounds, n=-2)

    # return MG_util.F_J(learned_f, K, rect, lower_bounds, n=-2)


morse_graph, map_graph = MG_util.run_CMGDB(
    subdiv_min, subdiv_max, lower_bounds, upper_bounds, phase_periodic, F, base_name, subdiv_init, cmap=newcmp)

# CMGDB.PlotMorseSets(morse_graph)

startTime = datetime.now()

roa = RoA.RoA(map_graph, morse_graph)

print(f"Time to build the regions of attraction = {datetime.now() - startTime}")

# roa.save_file(base_name)

fig, ax = roa.PlotTiles(cmap=newcmp)

# TM1 = NoisyTimeMap.NoisyTimeMap("examples/tripods/pendulum_noise.yaml")
#

# TM.duration = 0.1
#
# fig, ax = dyn_tools.Plot_trajectories(lower_bounds, upper_bounds, g, fig=fig, ax=ax, xlim=[
#                                       lower_bounds[0], upper_bounds[0]], ylim=[lower_bounds[1], upper_bounds[1]])

# RoA.PlotTiles(lower_bounds, upper_bounds,
#               from_file=base_name, from_file_basic=True)

plt.show()

# roa.save_file(base_name)
