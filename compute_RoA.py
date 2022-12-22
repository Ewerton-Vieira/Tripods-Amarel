import matplotlib
import CMGDB_util
import CMGDB
import RoA
import dyn_tools
import Grid
import sys
import ctypes

import NoisyTimeMap

import numpy as np

import matplotlib.pyplot as plt

from datetime import datetime


if __name__ == "__main__":

    if len(sys.argv) == 1:
        system_file_name = "examples/pendulum_lqr_noise.txt"
        # system_file_name = "examples/acrobot_lqr_noise.txt"
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

    # ######## Define the parameters example ################
    # sb = 14
    # time = 1
    # noise_level = 5
    # system = "pendulum_lqr"
    # yaml = "examples/tripods/pendulum_noise.yaml"
    #
    # phase_periodic = [True, False]
    # K = [1]*2  # Lipschitz
    # noise = [0.04]*2 # global noise = noise_x + noise_f + noise_u
    #
    # multivalued_map = "Box_noisy_K"
    # plot_RoA = True
    # ######## Define the parameters ################

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
    # time
    TM.duration = time
    ### noise ###

    names_noise = ['xt', 'f']

    parameters_upper_bounds = [TM.params["/plant/" + nname + "_noise_params"].as_float_vector()[1] for nname in names_noise]
    print(f"noise: xt & f = {parameters_upper_bounds}")

    # function of the underlying system and fixing the seed
    seed_base = TM.params["random_seed"].as_int()
    def g(X):
        TM.set_seed(ctypes.c_ulonglong(seed_base * hash(tuple(X))).value);
        return getattr(TM, TM.system_name)(X)

    MG_util = CMGDB_util.CMGDB_util()

    def F(rect):
        # X = rect[0:2]
        # if np.linalg.norm(np.array(g(X)) - np.array(g(X))) > 0.0000001:
        #     print("HERE FAIL")
        #     return False
        return getattr(MG_util, multivalued_map)(g, rect, K, noise)
        # return CMGDB.BoxMap(g, rect, padding=True)

    morse_graph, map_graph = MG_util.run_CMGDB(
        subdiv_min, subdiv_max, lower_bounds, upper_bounds, phase_periodic, F, base_name, subdiv_init)

    # CMGDB.PlotMorseSets(morse_graph)

    startTime = datetime.now()

    roa = RoA.RoA(map_graph, morse_graph)

    print(f"Time to build the regions of attraction = {datetime.now() - startTime}")

    roa.save_file(base_name)

    if plot_RoA: # plot

        fig, ax = roa.PlotTiles()
        ax.set_xlabel(r"$\theta$")
        ax.set_ylabel(r"$\dot\theta$")
        # base_name = "/output/" + base_name
        plt.savefig(base_name, bbox_inches='tight')
        plt.show()
