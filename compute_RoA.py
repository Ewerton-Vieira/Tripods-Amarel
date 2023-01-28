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
        system_file_name = "examples/quadrotor_lqr_noise.txt"
        # system_file_name = "examples/pendulum_lc_noise.txt"
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
    
    if config['data_input']:
        data_input = np.load(config['data_input'])


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


    MG_util = CMGDB_util.CMGDB_util()

    if config['data_input']:
        grid = Grid.Grid(lower_bounds, upper_bounds, sb)
        # id2image = grid.id2image(data_input)
  
        # def F(rect):
        #     return MG_util.F_data_wa(rect, id2image, grid.point2cell, K)

        file_name =  f"{os.path.abspath(os.getcwd())}/data/{base_name}_map_grid.csv"
        map = grid.load_map_grid(file_name)

        def g_on_grid(x):
            return grid.image_of_vertex_from_loaded_map(map, x)
        def F(rect):
            return getattr(MG_util, multivalued_map)(g_on_grid, rect, K, noise)
    else:
        # function of the underlying system and fixing the seed
        seed_base = TM.params["random_seed"].as_int()
        def g(X):
            vector = [np.around(a, 7) for a in X]
            vector = tuple(vector)
            TM.set_seed(ctypes.c_ulonglong(seed_base * hash(vector)).value)
            return getattr(TM, TM.system_name)(X)

        def F(rect):
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
        def g(X):
            return getattr(TM, TM.system_name)(X)

        fig, ax = roa.PlotTiles(cmap = cmap)

        if system[0:8] == "pendulum":

            TM.duration = 0.001
            fig, ax = dyn_tools.Plot_trajectories(lower_bounds, upper_bounds, g, fig=fig, ax=ax, xlim=[
                                                  lower_bounds[0], upper_bounds[0]], ylim=[lower_bounds[1], upper_bounds[1]])

            ax.set_xlabel(r"$\theta$")
            ax.set_ylabel(r"$\dot\theta$")

        elif system[0:9] == "quadrotor":

            # fig, ax = plt.subplots(figsize=(8, 8))



            TM.duration = 0.01
            fig, ax = dyn_tools.Plot_trajectories(lower_bounds, upper_bounds, g, fig=fig, ax=ax, xlim=[
                                                  lower_bounds[0], upper_bounds[0]], ylim=[lower_bounds[1], upper_bounds[1]])

            # plot trajectory
            # start_height, initial_velocity = (20, -14)
            # traj = [[start_height,initial_velocity]]
            # initial_point = [start_height,initial_velocity]
            # for i in range(100000):
            #         end_point = g(initial_point)
            #         traj.append(end_point)
            #         initial_point = end_point
            #
            # traj = np.array(traj)
            # print(traj[-1])
            #
            # plt.plot(traj[:,0],traj[:,1],color='blue')
            # plt.scatter(traj[0,0],traj[0,1],color='green')
            # plt.scatter(traj[-1,0],traj[-1,1],color='red')

            ax.set_xlabel(r"$x$")
            ax.set_ylabel(r"$\dot x$")

        else:
            fig, ax = roa.PlotTiles()

        base_name =  os.path.abspath(os.getcwd()) + "/output/" + base_name
        plt.savefig(base_name, bbox_inches='tight')
        plt.show()
