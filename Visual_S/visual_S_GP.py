# GP

# import Pendulum_lc as Pd

import CMGDB_util
import CMGDB
import RoA
import sys
import os

import numpy as np

from sklearn.multioutput import MultiOutputRegressor
from sklearn.gaussian_process import GaussianProcessRegressor
from sklearn.gaussian_process.kernels import RBF, WhiteKernel, Matern, ExpSineSquared, ConstantKernel


import matplotlib.pyplot as plt

from datetime import datetime


def learned_f(X):
    X = np.array(X).reshape(1, -1)
    y = dict()
    s = dict()
    for i in range(6):
        y[i], s[i] = gp[i].predict(X, return_std=True)
    y = np.concatenate((y[0], y[1], y[2], y[3], y[4], y[5]), axis=1)
    s = np.concatenate((s[0], s[1], s[2], s[3], s[4], s[5]), axis=0).reshape(1, -1)
    return y, s


def GP(X_train, Y_train):
    # fit Gaussian Process with dataset X_train, Y_train

    # DO #
    kernel = RBF()  # + WhiteKernel()  # define a kernel function here #

    # kernel = Matern() + WhiteKernel()

    # DO #
    n_restarts_optimizer = 5  # define a n_restarts_optimizerint value here #

    gp_ = GaussianProcessRegressor(kernel=kernel, n_restarts_optimizer=n_restarts_optimizer)

    # fit multi-response independently
    # multi_reg = MultiOutputRegressor(gp)
    # multi_reg.fit(X_train, Y_train)
    # return multi_reg

    gp_.fit(X_train, Y_train)
    return gp_


def MSE(X, Y):
    return np.linalg.norm(Y-X)/len(X)


def read_data(name_file):
    """Read and embbed"""
    X = []
    Y = []
    dir_path = os.path.abspath(os.getcwd()) + "/Visual_S/data/"
    name_file_ = dir_path + name_file
    with open(name_file_, 'r') as file:
        line = file.readline()

        while line != '':
            line_list = line.split()
            x, y, z = float(line_list[0]), float(line_list[1]), float(line_list[2])
            r, p, yaw = float(line_list[3]), float(line_list[4]), float(line_list[5])
            X.append([x, y, z, r, p, yaw])

            line = file.readline()
            line_list = line.split()
            x, y, z = float(line_list[0]), float(line_list[1]), float(line_list[2])
            r, p, yaw = float(line_list[3]), float(line_list[4]), float(line_list[5])
            Y.append([x, y, z, r, p, yaw])

            line = file.readline()

    return X, Y


if __name__ == "__main__":

    MG_util = CMGDB_util.CMGDB_util()

    sb = 20
    time = 0.8  # time is equal to 10s

    # subdiv_min = 10  # minimal subdivision to compute Morse Graph
    # subdiv_max = 10  # maximal subdivision to compute Morse Graph
    subdiv_init = subdiv_min = subdiv_max = sb  # non adaptive proceedure

    x_min = -1
    x_max = 1

    y_min = -1
    y_max = 1

    # base name for the output files.
    base_name = "Visual_S_GP_time" + \
        str(10*int(time)) + "_" + \
        str(subdiv_init)

    print(base_name)

    # Define the parameters for CMGDB
    lower_bounds = [x_min]*6
    upper_bounds = [x_max]*6

    # fig, ax = RoA.PlotTiles(lower_bounds, upper_bounds,
    #                         from_file=base_name)
    #
    # ax.set_xlabel("")
    # ax.set_ylabel("")
    # plt.savefig("out", bbox_inches='tight')
    # plt.show()

    # Load data from file

    X_train, Y_train = read_data("vs_trajs_new.txt")

    X_train = np.array(X_train)
    Y_train = np.array(Y_train)

    print(len(X_train))

    startTime = datetime.now()
    # train GP regression with X and Y
    gp = dict()
    for i in range(6):
        gp[i] = GP(X_train, Y_train[:, i].reshape(-1, 1))
    print(f"Time to train GP = {datetime.now() - startTime}")
    # prediction function

    Y = [learned_f(x_)[0][0] for x_ in X_train]
    Y = np.array(Y)

    print(MSE(Y_train, Y))

    #[-0.0142023, -0.00733125, 0.770845, -0.0377398, 0.00389325, -0.0283213]
    #[-0.0136244, -0.00703399, 0.770026, -0.0362455, 0.00370949, -0.0271537]
    print(learned_f([-0.0142023, -0.00733125, 0.770845, -0.0377398, 0.00389325, -0.0283213]))

    # X = []
    # for i in np.linspace(lower_bounds[0], upper_bounds[0], 10):
    #     for j in np.linspace(lower_bounds[1], upper_bounds[1], 10):
    #         for ii in np.linspace(lower_bounds[2], upper_bounds[2], 10):
    #             for jj in np.linspace(lower_bounds[3], upper_bounds[3], 10):
    #                 for iii in np.linspace(lower_bounds[4], upper_bounds[4], 10):
    #                     for jjj in np.linspace(lower_bounds[5], upper_bounds[5], 10):
    #                         X.append([i, j, ii, jj, iii, jjj])
    #
    # X = np.array(X)
    # Y = [learned_f(x_)[0][0] for x_ in X]
    # Y = np.array(Y)

    K = 1

    phase_periodic = [False]*6
    #
    # def g(X):
    #     return learned_f(X)[0].tolist()[0]
    #
    # print(g([2, 1.6]))
    #

    def F(rect):
        # return MG_util.Box_GP_K(learned_f, rect, K)
        # return CMGDB.BoxMap(g, rect, padding=True)
        # return MG_util.F_K(g, rect, K)
        # return MG_util.BoxMapK(g_on_grid, rect, K)
        return MG_util.Box_ptwise(learned_f, rect, n=-2)
    #
    morse_graph, map_graph = MG_util.run_CMGDB(
        subdiv_min, subdiv_max, lower_bounds, upper_bounds, phase_periodic, F, base_name, subdiv_init)

    # CMGDB.PlotMorseSets(morse_graph)

    startTime = datetime.now()

    roa = RoA.RoA(map_graph, morse_graph)

    print(f"Time to build the regions of attraction = {datetime.now() - startTime}")

    roa.save_file(base_name)
    #
    # fig, ax = roa.PlotTiles()
    #
    # ax.set_xlabel(r"$h$")
    # ax.set_ylabel(r"$\dot h$")
    # ax.set_xlabel("")
    # ax.set_ylabel("")
    # plt.savefig("out", bbox_inches='tight')
    # plt.show()
    # ########
