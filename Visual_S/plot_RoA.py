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


    system_file_name = "input.txt"

    with open(system_file_name, 'r') as f:
        config = eval(f.read())

    ######## Define the parameters ################
    sb = int(config['sb'])
    time = float(config['time'])  # propagation is 0.04
    noise_level = int(config['noise_level'])
    system = config['system']
    name_file = config['name_file']

    phase_periodic = [bool(a) for a in config['phase_periodic'].split()]
    K = [float(a) for a in config['K'].split()] # Lipschitz
    noise = [float(a) for a in config['noise'].split()] # global noise = [noise_x + noise_f + noise_u]*dim

    multivalued_map = config['multivalued_map']
    plot_RoA = int(config['plot_RoA'])

    skip = int(config['skip'])
    ######## Define the parameters ################

    time_step = int(np.around(time / 0.04))

    # Define the parameters for CMGDB
    lower_bounds = [-0.3, -0.3, 0.5, -1.17866, -1.17866, -1.17866]
    upper_bounds = [0.3, 0.3, 1, 1.17866, 1.17866, 1.17866]

    subdiv_init = subdiv_min = subdiv_max = sb  # non adaptive proceedure


    # base name for the output files.
    base_name = f"Visual_S_time_{time_step}_{skip}_{subdiv_init}"

    print(base_name)

    section = ([2,3,4,5],(0,0,0.75,0,0,0))

    # section = ([2,3,4,5], 'projection')

    # fig, ax = RoA.PlotTiles(lower_bounds, upper_bounds, name_plot=base_name, from_file=base_name, section=section)

    # PlotTiles(lower_bounds, upper_bounds, selection=[], fig_w=8, fig_h=8, xlim=None, ylim=None, fontsize=16,
    #               cmap=matplotlib.cm.get_cmap('viridis', 256), name_plot=' ', from_file=None, plot_point=False, section=None, from_file_basic=False)

    fig, ax, d_vol = RoA.PlotTiles(lower_bounds, upper_bounds, name_plot=base_name, from_file=base_name, section=section)
    print(d_vol[0])

    plt.plot()
