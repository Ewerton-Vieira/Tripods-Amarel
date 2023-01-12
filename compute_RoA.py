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
        system_file_name = "examples/quadrotor_lqr_noise.txt"
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

    if config['color_map'] == 'friendly':
        cmap = friendly_colors()
    else:
        cmap = matplotlib.cm.get_cmap('viridis', 256)



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

    names_noise = ['xt', 'ft']


    parameters_upper_bounds = [TM.params["/plant/" + nname + "_noise_params"].as_float_vector()[1] for nname in names_noise]
    print(f"noise: xt & ft = {parameters_upper_bounds}")

    # function of the underlying system and fixing the seed
    seed_base = TM.params["random_seed"].as_int()
    def g(X):
        # vector = [np.around(a, 7) for a in X]
        # vector = tuple(vector)
        # TM.set_seed(ctypes.c_ulonglong(seed_base * hash(vector)).value)
        return getattr(TM, TM.system_name)(X)


    # print('HERE', TM.system_name,  g([5,5]))
    #
    #
    MG_util = CMGDB_util.CMGDB_util()

    def F(rect):
        # X = rect[0:2]
        # if np.linalg.norm(np.array(g(X)) - np.array(g(X))) > 0.0000001:
        #     print("HERE FAIL")
        #     return False
        return getattr(MG_util, multivalued_map)(g, rect, K, noise)
        # return CMGDB.BoxMap(g, rect, padding=True)

    morse_graph, map_graph = MG_util.run_CMGDB(
        subdiv_min, subdiv_max, lower_bounds, upper_bounds, phase_periodic, F, base_name, subdiv_init, cmap = cmap)

    # CMGDB.PlotMorseSets(morse_graph)

    startTime = datetime.now()

    roa = RoA.RoA(map_graph, morse_graph)

    print(f"Time to build the regions of attraction = {datetime.now() - startTime}")

    roa.save_file(base_name)

    if plot_RoA: # plot

        fig, ax = roa.PlotTiles(cmap = cmap)

        if system[0:8] == "pendulum":

            TM.duration = 0.001
            fig, ax = dyn_tools.Plot_trajectories(lower_bounds, upper_bounds, g, fig=fig, ax=ax, xlim=[
                                                  lower_bounds[0], upper_bounds[0]], ylim=[lower_bounds[1], upper_bounds[1]])

            ax.set_xlabel(r"$\theta$")
            ax.set_ylabel(r"$\dot\theta$")

        elif system[0:9] == "quadrotor":

            fig, ax = plt.subplots(figsize=(8, 8))

            TM.duration = 0.1
            fig, ax = dyn_tools.Plot_trajectories(lower_bounds, upper_bounds, g, fig=fig, ax=ax, xlim=[
                                                  lower_bounds[0], upper_bounds[0]], ylim=[lower_bounds[1], upper_bounds[1]])

            ax.set_xlabel(r"$x$")
            ax.set_ylabel(r"$\dot x$")

        else:
            fig, ax = roa.PlotTiles()

        # base_name = "/output/" + base_name
        plt.savefig(base_name, bbox_inches='tight')
        plt.show()
