import CMGDB_util
import CMGDB
import Grid
import RoA
import sys
import os

import numpy as np

import matplotlib.pyplot as plt

from datetime import datetime


def read_data(name_file):
    """Read and embbed"""
    X = []
    Y = []
    dir_path = os.path.abspath(os.getcwd()) + "/data/"
    name_file_ = dir_path + name_file
    with open(name_file_, 'r') as file:
        line_x = file.readline()
        line_y = file.readline()


        while line_x != '' and line_y != '':

            line_list_x = line_x.split()
            line_list_y = line_y.split()

            if len(line_list_x) == 7 and len(line_list_y) == 7:
                x, y, z = float(line_list_x[0]), float(line_list_x[1]), float(line_list_x[2])
                r, p, yaw = float(line_list_x[3]), float(line_list_x[4]), float(line_list_x[5])
                X.append([x, y, z, r, p, yaw])

                x, y, z = float(line_list_y[0]), float(line_list_y[1]), float(line_list_y[2])
                r, p, yaw = float(line_list_y[3]), float(line_list_y[4]), float(line_list_y[5])
                Y.append([x, y, z, r, p, yaw])

            line_x = file.readline()
            line_y = file.readline()

    return X, Y


if __name__ == "__main__":

    MG_util = CMGDB_util.CMGDB_util()

    sb = 20
    time = 1.2  # propagation is 0.04

    ### file name and parameters ###
    skip=20
    time_step=30
    name_file = "data_vs"

    # subdiv_min = 10  # minimal subdivision to compute Morse Graph
    # subdiv_max = 10  # maximal subdivision to compute Morse Graph
    subdiv_init = subdiv_min = subdiv_max = sb  # non adaptive proceedure


    # base name for the output files.
    base_name = "Visual_S_time" + \
        str(int(10*time)) + "_" + \
        str(subdiv_init)

    print(base_name)

    # Define the parameters for CMGDB
    lower_bounds = [-0.3, -0.3, -0.5, -1.17866, -1.17866, -1.17866]
    upper_bounds = [0.3, 0.3, 0.5, 1.17866, 1.17866, 1.17866]
    phase_periodic = [False]*6


    # Load data from file

    X, f_X = read_data(f"{name_file}_{skip}_{time_step}")

    X = np.array(X)
    f_X = np.array(f_X)

    data = np.concatenate((X,f_X),axis=1)

    print(len(X))

    grid = Grid.Grid(lower_bounds, upper_bounds, sb)

    print(data.shape)

    id2image = grid.id2image(data)

    print(len(id2image))

    count = 0
    for i in id2image:
        if len(i) == 0:
            count += 1
    print(f'Empty boxes = {count}')


    # Define box map for the data
    K=[1] * grid.dim
    def F(rect):
        return MG_util.F_data(rect, id2image, grid.point2cell, K)
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
