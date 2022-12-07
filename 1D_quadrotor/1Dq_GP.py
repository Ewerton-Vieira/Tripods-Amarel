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


def pplot(x_add, y_add, base_name="out"):

    fig_w = 8
    fig_h = 8
    fig1, ax1 = plt.subplots(figsize=(fig_w, fig_h))

    COLOR_X = 'r.'

    COLOR_Y = 'bx'
    LABEL_X = 'Initial points'
    LABEL_Y = 'Endpoints'

    ax1.plot(x_add[:, 0], x_add[:, 1], COLOR_X, label='Initial points')
    ax1.plot(y_add[:, 0], y_add[:, 1], COLOR_Y, label='Endpoints')

    tick = 5  # tick for 2D plots
    d1 = 0
    d2 = 1

    fontsize = 32

    plt.xticks(np.linspace(lower_bounds[d1], upper_bounds[d1], tick))
    plt.yticks(np.linspace(lower_bounds[d2], upper_bounds[d2], tick))

    ax1.set_xlabel(r"$h$")
    ax1.set_ylabel(r"$\dot h$")
    plt.xticks(fontsize=fontsize)
    plt.yticks(fontsize=fontsize)
    ax1.xaxis.label.set_size(fontsize)
    ax1.yaxis.label.set_size(fontsize)

    outpath = os.path.abspath(os.getcwd()) + "/output/"

    plt.savefig(outpath + base_name + "_data_" + str(len(x_add)) + ".png", bbox_inches='tight')
    plt.show()


def read_data_1Dq(skip=1, N_files=100):
    """Read and embbed"""
    X = []
    Y = []
    dir_path = os.path.abspath(os.getcwd()) + "/1D_quadrotor/data/"
    for i in range(N_files):
        name_file = dir_path + str(i) + ".txt"
        X_temp = []
        with open(name_file, 'r') as file:
            k = 0
            line = file.readline()
            while line != '':

                if k % skip:
                    pass
                else:
                    line_list = line[1:-2].split()
                    x, y = float(line_list[0]), float(line_list[1])
                    X_temp.append([x, y])
                k += 1
                line = file.readline()
        X += X_temp[0:-1]
        Y += X_temp[1::]
    return X, Y


if __name__ == "__main__":

    MG_util = CMGDB_util.CMGDB_util()

    sb = 14
    time = 0.5  # time is equal to 10s

    # subdiv_min = 10  # minimal subdivision to compute Morse Graph
    # subdiv_max = 10  # maximal subdivision to compute Morse Graph
    subdiv_init = subdiv_min = subdiv_max = sb  # non adaptive proceedure

    x_min = 0
    x_max = 2

    y_min = -0.5
    y_max = 1.5

    # base name for the output files.
    base_name = "1Dq_GP_time" + \
        str(10*time) + "_" + \
        str(subdiv_init)

    print(base_name)

    # Define the parameters for CMGDB
    lower_bounds = [x_min, y_min]
    upper_bounds = [x_max, y_max]

    # fig, ax = RoA.PlotTiles(lower_bounds, upper_bounds,
    #                         from_file=base_name)
    #
    # ax.set_xlabel("")
    # ax.set_ylabel("")
    # plt.savefig("out", bbox_inches='tight')
    # plt.show()

    # Load data from file

    X_train, Y_train = read_data_1Dq(20*time)

    X_train = np.array(X_train)
    Y_train = np.array(Y_train)

    print(len(X_train))

    # Define a Gaussian process

    def GP(X_train, Y_train):
        # fit Gaussian Process with dataset X_train, Y_train

        # DO #
        kernel = RBF()  # define a kernel function here #

        kernel = Matern() + WhiteKernel()

        # DO #
        n_restarts_optimizer = 5  # define a n_restarts_optimizerint value here #

        gp_ = GaussianProcessRegressor(kernel=kernel, n_restarts_optimizer=n_restarts_optimizer)

        # fit multi-response independently
        # multi_reg = MultiOutputRegressor(gp)
        # multi_reg.fit(X_train, Y_train)
        # return multi_reg

        gp_.fit(X_train, Y_train)
        return gp_

    # train GP regression with X and Y
    gp1 = GP(X_train, Y_train[:, 0].reshape(-1, 1))

    gp2 = GP(X_train, Y_train[:, 1].reshape(-1, 1))

    # prediction function

    def learned_f(X):
        X = np.array(X).reshape(1, -1)
        y1, s1 = gp1.predict(X, return_std=True)
        y2, s2 = gp2.predict(X, return_std=True)
        return np.concatenate((y1, y2), axis=1), np.concatenate((s1, s2), axis=0).reshape(1, -1)

    X = []
    for i in np.linspace(lower_bounds[0], upper_bounds[0], 20):
        for j in np.linspace(lower_bounds[1], upper_bounds[1], 20):
            X.append([i, j])

    # grid_X, grid_Y = np.meshgrid(grid_x, grid_y)

    # print(grid_X[0])
    X = np.array(X)
    Y = [learned_f(x_)[0][0] for x_ in X]
    Y = np.array(Y)

    pplot(X, Y, base_name=base_name)
    # ############
    #
    # print(learned_f([2, 1.6]))
    #
    # K = 1
    #
    # phase_periodic = [False, False]
    #
    # def g(X):
    #     return learned_f(X)[0].tolist()[0]
    #
    # print(g([2, 1.6]))
    #
    # def F(rect):
    #     # return MG_util.Box_GP_K(learned_f, rect, K)
    #     # return CMGDB.BoxMap(g, rect, padding=True)
    #     # return MG_util.F_K(g, rect, K)
    #     # return MG_util.BoxMapK(g_on_grid, rect, K)
    #     return MG_util.Box_ptwise(learned_f, rect, n=-2)
    #
    # morse_graph, map_graph = MG_util.run_CMGDB(
    #     subdiv_min, subdiv_max, lower_bounds, upper_bounds, phase_periodic, F, base_name, subdiv_init)
    #
    # # CMGDB.PlotMorseSets(morse_graph)
    #
    # startTime = datetime.now()
    #
    # roa = RoA.RoA(map_graph, morse_graph)
    #
    # print(f"Time to build the regions of attraction = {datetime.now() - startTime}")
    #
    # roa.save_file(base_name)
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
"""
    def F(rect):
        return MG_util.F_GP_K(learned_f, rect, K)
        # return CMGDB.BoxMap(g, rect, padding=True)
        # return MG_util.F_K(g, rect, K)
        # return MG_util.BoxMapK(g_on_grid, rect, K)

    morse_graph, map_graph = MG_util.run_CMGDB(
        subdiv_min, subdiv_max, lower_bounds, upper_bounds, phase_periodic, F, base_name, subdiv_init)

    # CMGDB.PlotMorseSets(morse_graph)

    startTime = datetime.now()

    roa = RoA.RoA(map_graph, morse_graph)

    print(f"Time to build the regions of attraction = {datetime.now() - startTime}")

    # roa.save_file(base_name)

    fig, ax = roa.PlotTiles()

    # RoA.PlotTiles(lower_bounds, upper_bounds,
    #               from_file=base_name, from_file_basic=True)

    # plt.show()

    # roa.save_file(base_name)

  ##########

    def g(X):
        Y, _ = learned_f(X)
        return Y.tolist()[0]

    def F(rect):
        # return MG_util.Box_GP_K(learned_f, rect, K)
        return CMGDB.BoxMap(g, rect, padding=True)
        # return MG_util.F_K(g, rect, K)
        # return MG_util.BoxMapK(g_on_grid, rect, K)

    morse_graph, map_graph = MG_util.run_CMGDB(
        subdiv_min, subdiv_max, lower_bounds, upper_bounds, phase_periodic, F, base_name, subdiv_init)

    # CMGDB.PlotMorseSets(morse_graph)

    startTime = datetime.now()

    roa = RoA.RoA(map_graph, morse_graph)

    print(f"Time to build the regions of attraction = {datetime.now() - startTime}")

    # roa.save_file(base_name)

    fig, ax = roa.PlotTiles()

    # RoA.PlotTiles(lower_bounds, upper_bounds,
    #               from_file=base_name, from_file_basic=True)

    plt.show()
"""
