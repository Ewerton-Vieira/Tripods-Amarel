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

    if len(sys.argv) == 1:
        # system_file_name = "examples/pendulum_lqr_noise.txt"
        system_file_name = "examples/acrobot_lqr_noise.txt"
    else:
        system_file_name = sys.argv[1]


    with open(system_file_name, 'r') as f:
        config = eval(f.read())

    ######## Define the parameters ################
    sb = int(config['sb'])
    time = float(config['time'])
    noise_level = int(config['noise_level'])
    system = config['system']
    yaml = config['yaml']

    phase_periodic = [bool(a) for a in config['phase_periodic'].split()]
    K = [float(a) for a in config['K'].split()] # Lipschitz
    noise = [float(a) for a in config['noise'].split()] # global noise = [noise_x + noise_f + noise_u]*dim

    multivalued_map = config['multivalued_map']
    plot_RoA = int(config['plot_RoA'])
    ######## Define the parameters ################


    subdiv_init = subdiv_min = subdiv_max = sb  # non adaptive proceedure
    # base name for the output files.
    base_name = f"{system}_t{int(10*time)}_sb{subdiv_init}_ns{noise_level}"

    print(base_name)


    # load map
    TM = NoisyTimeMap.NoisyTimeMap(yaml)
    print(f"system: {TM.system_name}")
    # bounds
    TM.ss.print_bounds()
    lower_bounds = TM.ss.get_lower_bounds()
    upper_bounds = TM.ss.get_upper_bounds()

    name_file = base_name + "_RoA_.csv"

    section = ([2,3,4,5],(0,0,0,0,0,0))

    fig, ax = RoA.PlotTiles(lower_bounds, upper_bounds, name_plot=base_name, from_file=name_file)

    # PlotTiles(lower_bounds, upper_bounds, selection=[], fig_w=8, fig_h=8, xlim=None, ylim=None, fontsize=16,
    #               cmap=matplotlib.cm.get_cmap('viridis', 256), name_plot=' ', from_file=None, plot_point=False, section=None, from_file_basic=False)

    plt.plot()
