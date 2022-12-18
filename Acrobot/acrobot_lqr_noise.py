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

    ######## Define the parameters ################
    sb = 14
    time = 1
    noise_level = 5
    system = "pendulum_lqr"
    yaml = "examples/tripods/pendulum_noise.yaml"

    phase_periodic = [True, False]
    K = [1]*2  # Lipschitz
    noise = [0.04]*2 # global noise = noise_x + noise_f + noise_u

    multivalued_map = "Box_noisy_K"
    plot_RoA = True
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
    # time
    TM.duration = time
    # noise
    names_noise = ['x_0', 'u_t','t','f']
    parameters_upper_bounds = [TM.params[nname + "_noise_params"].as_float_vector()[1] for nname in names_noise]
    print(f"noise: x & u_t & t & f = {parameters_upper_bounds}")

    # function of the underlying system
    g = getattr(TM, TM.system_name)

    MG_util = CMGDB_util.CMGDB_util()

    def F(rect):
        return getattr(MG_util, multivalued_map)(g, rect, K, noise)
        # return CMGDB.BoxMap(g, rect, padding=True)

    morse_graph, map_graph = MG_util.run_CMGDB(
        subdiv_min, subdiv_max, lower_bounds, upper_bounds, phase_periodic, F, base_name, subdiv_init)

    # CMGDB.PlotMorseSets(morse_graph)

    startTime = datetime.now()

    roa = RoA.RoA(map_graph, morse_graph)

    print(f"Time to build the regions of attraction = {datetime.now() - startTime}")

    roa.save_file(base_name)

    fig, ax = roa.PlotTiles()

    if plot_RoA: # plot
        plt.show()
