import matplotlib
import CMGDB_util
import CMGDB
import RoA
import dyn_tools
import Grid
import sys

import NoisyTimeMap

import numpy as np

import matplotlib.pyplot as plt

from datetime import datetime


if __name__ == "__main__":


    sb = 20
    time = 1.2  # time is equal to 10s

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


    section = ([2,3,4,5],(0,0,0,0,0,0))

    # section = ([2,3,4,5], 'projection')

    fig, ax = RoA.PlotTiles(lower_bounds, upper_bounds, name_plot=base_name, from_file=base_name, section=section)

    # PlotTiles(lower_bounds, upper_bounds, selection=[], fig_w=8, fig_h=8, xlim=None, ylim=None, fontsize=16,
    #               cmap=matplotlib.cm.get_cmap('viridis', 256), name_plot=' ', from_file=None, plot_point=False, section=None, from_file_basic=False)

    plt.plot()
