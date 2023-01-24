import matplotlib
import CMGDB_util
import CMGDB
import RoA
import dyn_tools
import sys
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
        system_file_name = "examples/traj_tracking_full.txt"
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
    ######## Define the parameters ################


    subdiv_init = subdiv_min = subdiv_max = sb  # non adaptive proceedure
    # base name for the output files.

    # load map
    TM = NoisyTimeMap.NoisyTimeMap(yaml)
    print(f"system: {TM.system_name}")
    # bounds
    TM.ss.print_bounds()
    lower_bounds = TM.ss.get_lower_bounds()
    upper_bounds = TM.ss.get_upper_bounds()

    base_name = f"{system}_traj_full_t{int(10*time)}_sb{subdiv_init}_ns{noise_level}"
    print(base_name)

    # time
    TM.duration = time
    ### noise ###
    names_noise = ['xt', 'ft']
    parameters_upper_bounds = [TM.params["/plant/" + nname + "_noise_params"].as_float_vector()[1] for nname in names_noise]
    print(f"noise: xt & ft = {parameters_upper_bounds}")

    ### function ###
    def g(X):
        return TM.pendulum_trajectory_ilqr(X)

    
    MG_util = CMGDB_util.CMGDB_util()

    def F(rect):
        # X = rect[0:2]
        # if np.linalg.norm(np.array(g(X)) - np.array(g(X))) > 0.0000001:
        #     print("HERE FAIL")
        #     return False
        # return getattr(MG_util, multivalued_map)(g, rect, K, noise)
        return CMGDB.BoxMap(g, rect, padding=True)

    morse_graph, map_graph = MG_util.run_CMGDB(
        subdiv_min, subdiv_max, lower_bounds, upper_bounds, phase_periodic, F, base_name, subdiv_init, cmap = cmap)

    # CMGDB.PlotMorseSets(morse_graph)

    startTime = datetime.now()

    roa = RoA.RoA(map_graph, morse_graph)

    print(f"Time to build the regions of attraction = {datetime.now() - startTime}")

    # roa.save_file(base_name)

    if plot_RoA: # plot

        fig, ax = roa.PlotTiles(cmap = cmap)

        if system[0:8] == "pendulum":

            TM.duration = 0.03
            fig, ax = dyn_tools.Plot_trajectories(lower_bounds, upper_bounds, g, fig=fig, ax=ax, xlim=[
                                                  lower_bounds[0], upper_bounds[0]], ylim=[lower_bounds[1], upper_bounds[1]])

            ax.set_xlabel(r"$\theta$")
            ax.set_ylabel(r"$\dot\theta$")

        else:
            fig, ax = roa.PlotTiles()
        

        base_name =  os.path.abspath(os.getcwd()) + "/output/" + base_name
        plt.savefig(base_name, bbox_inches='tight')
        plt.show()
