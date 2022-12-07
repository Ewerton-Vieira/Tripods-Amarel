# GP

# import Pendulum_lc as Pd

import CMGDB_util
import CMGDB
import RoA
import sys
import os

import numpy as np

import GPy

import matplotlib.pyplot as plt

from datetime import datetime


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

    # Load data from file

    X_train, Y_train = read_data_1Dq(60*time)

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

    ############

    print(learned_f([2, 1.6]))

    K = 1

    phase_periodic = [False, False]

    def g(X):
        return learned_f(X)[0].tolist()[0]

    print(g([2, 1.6]))

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

    # roa.save_file(base_name)

    ########
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
