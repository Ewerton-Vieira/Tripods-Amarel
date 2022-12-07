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


sb = 10
time = 10  # time is equal to time * 0.1s

# subdiv_min = 10  # minimal subdivision to compute Morse Graph
# subdiv_max = 10  # maximal subdivision to compute Morse Graph
subdiv_init = subdiv_min = subdiv_max = sb  # non adaptive proceedure


# base name for the output files.
base_name = "mountain_car_lc_time" + \
    str(time) + "_" + \
    str(subdiv_init)


print(base_name)


# load map
# set the time step
TM = TimeMap.TimeMap("mountain_car_lc", time,
                     "examples/tripods/mountain_car_lc.yaml")
# TM.duration = time
# define the lqr time map for the pendulum


# Define the parameters for CMGDB
TM.ss.print_bounds()
lower_bounds = TM.ss.get_lower_bounds()
upper_bounds = TM.ss.get_upper_bounds()

print(lower_bounds, upper_bounds)


def g(X):
    return TM.mountain_car_lc(X)


def sample_points(lower_bounds, upper_bounds, num_pts):
    # Sample num_pts in dimension dim, where each
    # component of the sampled points are in the
    # ranges given by lower_bounds and upper_bounds
    dim = len(lower_bounds)
    X = np.random.uniform(lower_bounds, upper_bounds, size=(num_pts, dim))
    return X


def plot_data(X, Y, COLOR_X='ro', COLOR_Y='bx', LABEL_X='Initial points', LABEL_Y='Endpoints', xlabel='x', ylabel='y', d=4, arrow=False, mixed_variables=False):  # d = dimension
    fig = plt.figure(figsize=(10, 10))

    COLOR_ARROW = 'lightgray'

    plt.subplot(2, 2, 1)
    d1 = 0
    d2 = 1
    plt.plot(X[:, d1], X[:, d2], COLOR_X, label=LABEL_X)
    plt.plot(Y[:, d1], Y[:, d2], COLOR_Y, label=LABEL_Y)
    # plt.xlabel('x[' + str(d1) +']');
    # plt.ylabel('x[' + str(d2) +']');
    plt.xlabel(xlabel)
    plt.ylabel(ylabel)
    plt.legend()
    # plt.grid()

    if arrow:
        for k in range(len(X[:, d1])):
            plt.arrow(X[:, d1][k], X[:, d2][k], Y[:, d1][k] -
                      X[:, d1][k], Y[:, d2][k] - X[:, d2][k], color=COLOR_ARROW)

    if d > 2:
        plt.subplot(2, 2, 2)
        d1 = 2
        d2 = 3
        plt.plot(X[:, d1], X[:, d2], COLOR_X, label=LABEL_X)
        plt.plot(Y[:, d1], Y[:, d2], COLOR_Y, label=LABEL_Y)
        plt.legend()
        # plt.grid()
        # plt.xlabel('x[' + str(d1) +']');
        # plt.ylabel('x[' + str(d2) +']');
        plt.xlabel('theta_dot 1')
        plt.ylabel('theta_dot 2')
        if arrow:
            for k in range(len(X[:, d1])):
                plt.arrow(X[:, d1][k], X[:, d2][k], Y[:, d1][k] -
                          X[:, d1][k], Y[:, d2][k] - X[:, d2][k], color=COLOR_ARROW)

        if mixed_variables:

            plt.subplot(2, 2, 3)
            d1 = 0
            d2 = 2
            plt.plot(X[:, d1], X[:, d2], COLOR_X, label=LABEL_X)
            plt.plot(Y[:, d1], Y[:, d2], COLOR_Y, label=LABEL_Y)
            plt.legend()
            # plt.grid()
            # plt.xlabel('x[' + str(d1) +']');
            # plt.ylabel('x[' + str(d2) +']');
            plt.xlabel('theta 1')
            plt.ylabel('theta_dot 1')
            if arrow:
                for k in range(len(X[:, d1])):
                    plt.arrow(X[:, d1][k], X[:, d2][k], Y[:, d1][k] -
                              X[:, d1][k], Y[:, d2][k] - X[:, d2][k], color=COLOR_ARROW)

            plt.subplot(2, 2, 4)
            d1 = 1
            d2 = 3
            plt.plot(X[:, d1], X[:, d2], COLOR_X, label=LABEL_X)
            plt.plot(Y[:, d1], Y[:, d2], COLOR_Y, label=LABEL_Y)
            plt.legend()
            # plt.grid()
            # plt.xlabel('x[' + str(d1) +']');
            # plt.ylabel('x[' + str(d2) +']');
            plt.xlabel('theta 2')
            plt.ylabel('theta_dot 2')
            if arrow:
                for k in range(len(X[:, d1])):
                    plt.arrow(X[:, d1][k], X[:, d2][k], Y[:, d1][k] -
                              X[:, d1][k], Y[:, d2][k] - X[:, d2][k], color=COLOR_ARROW)

        # Adjust spacing between subplots
        plt.subplots_adjust(hspace=0.2, wspace=0.3)
    plt.show()


num_pts = 10000

X = sample_points(lower_bounds, upper_bounds, num_pts)

Y = [g(x) for x in X]
Y = np.array(Y)


plot_data(X, Y, xlabel=r"$x$", ylabel=r"$\dot x$", d=2)
