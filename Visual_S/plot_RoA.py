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



# d = {2: 0.009696447878905948, 7: 0.01562715913622714, 6: 0.01300633837206832, 3: 0.02022684681445422, 0: 0.015643649693844342, 1: 0.008780044034179854, 5: 0.007586834400879516, 4: 0.0037551355488279264}

d = {3: 0.014913059096546456, 0: 0.01263942346508124, 13: 0.009180529004883023, 14: 0.01102835488073385, 9: 0.0061262421547864584, 1: 0.008097158264284586, 2: 0.00828709415112503, 4: 0.0041205780845941, 29: 1.1778969726562496e-06, 23: 5.889484863281248e-07, 5: 1.7668454589843744e-06, 24: 8.834227294921872e-07, 6: 8.834227294921872e-07, 21: 5.889484863281248e-07, 7: 2.944742431640624e-07, 8: 2.944742431640624e-07, 10: 2.944742431640624e-07, 11: 2.944742431640624e-07, 12: 2.944742431640624e-07, 15: 2.944742431640624e-07, 16: 2.944742431640624e-07, 17: 2.944742431640624e-07, 18: 2.944742431640624e-07, 19: 2.944742431640624e-07, 20: 2.944742431640624e-07, 22: 2.944742431640624e-07, 25: 2.944742431640624e-07, 26: 2.944742431640624e-07, 27: 2.944742431640624e-07, 28: 2.944742431640624e-07, 30: 2.944742431640624e-07, 31: 2.944742431640624e-07}

value = 0
for k, v in d.items():
    value += v
print(value)


if __name__ == "__main_1_":


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

    fig, ax = RoA.PlotTiles(lower_bounds, upper_bounds, name_plot=base_name, from_file=base_name, section=section)

    # fig, ax, d_vol = RoA.PlotTiles(lower_bounds, upper_bounds, name_plot=base_name, from_file=base_name, section=section)
    # print(d_vol[0])

    plt.plot()
