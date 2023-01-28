import matplotlib
import CMGDB_util
import CMGDB
import RoA
import dyn_tools
import Grid
import sys
import ctypes
import os

import NoisyTimeMap

import numpy as np

import matplotlib.pyplot as plt
import matplotlib

from datetime import datetime

def friendly_colors():
    # friendly colors
    viridis = matplotlib.cm.get_cmap('viridis', 256)
    newcolors = viridis(np.linspace(0, 1, 256))
    orange = np.array([253/256, 174/256, 97/256, 1])
    yellowish = np.array([233/256, 204/256, 50/256, 1])
    newcolors[109:146, :] = orange
    newcolors[219:, :] = yellowish
    newcmp = matplotlib.colors.ListedColormap(newcolors)
    return newcmp

if __name__ == "__main__":

    if len(sys.argv) == 1:
        # system_file_name = "examples/pendulum_lqr_noise.txt"
        # system_file_name = "examples/acrobot_lqr_noise.txt"
        # system_file_name = "examples/quadrotor_lqr_noise.txt"
        system_file_name = "examples/pendulum_lc_noise.txt"
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

    phase_periodic = [bool(int(a)) for a in config['phase_periodic'].split()]
    K = [float(a) for a in config['K'].split()] # Lipschitz
    noise = [float(a) for a in config['noise'].split()] # global noise = [noise_x + noise_f + noise_u]*dim

    multivalued_map = config['multivalued_map']
    plot_RoA = int(config['plot_RoA'])

    if config['color_map'] == 'friendly':
        cmap = friendly_colors()
    else:
        cmap = matplotlib.cm.get_cmap('viridis', 256)




    subdiv_init = subdiv_min = subdiv_max = sb  # non adaptive proceedure
    # base name for the output files.
    base_name = f"{system}_t{int(10*time)}_data"

    print(base_name)

    # load map
    TM = NoisyTimeMap.NoisyTimeMap(yaml)
    print(f"system: {TM.system_name}")
    # bounds
    TM.ss.print_bounds()
    lower_bounds = TM.ss.get_lower_bounds()
    upper_bounds = TM.ss.get_upper_bounds()
    # time
    TM.duration = time
    ### noise ###

    names_noise = ['xt', 'ft']


    parameters_upper_bounds = [TM.params["/plant/" + nname + "_noise_params"].as_float_vector()[1] for nname in names_noise]
    print(f"noise: xt & ft = {parameters_upper_bounds}")

    # function of the underlying system
    def g(X):
        return getattr(TM, TM.system_name)(X)


    # print('HERE', TM.system_name,  g([5,5]))


    grid = Grid.Grid(lower_bounds, upper_bounds, sb)

    data_x = grid.uniform_sample()

    # plt.scatter(data_x[:,0], data_x[:,1])

    data_fx =  np.array([g(x_.tolist()) for x_ in data_x])

    # plt.scatter(data_fx[:,0], data_fx[:,1])

    # plt.show()

    data = np.concatenate((data_x, data_fx), axis=1)

    np.save(base_name, data) 