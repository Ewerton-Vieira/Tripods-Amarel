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

def transf(X, shift):
    X[0] += shift
    if X[0] >= pi:
        X[0] -= 2*pi
    return X

def inv_transf(X, shift):
    X[0] -= shift
    if X[0] <= -pi:
        X[0] += 2*pi
    return X

def funnel(roa, lower_bounds, upper_bounds, local_goal):

    dict_tiles = roa.dict_tiles
    number_vertices_MG = roa.num_verts
    rect = roa.morse_graph.phase_space_box(0)
    dim = int(len(rect) // 2)
    size_box = [rect[dim + i] - rect[i] for i in range(dim)]
    phase_space_box = roa.morse_graph.phase_space_box
    largest_length = list(rect)  # initalizing the largest length for each dimension
    
    for tile, morse_node in dict_tiles.items():
        if morse_node == -1:
            continue
        for count, value in enumerate(phase_space_box(tile)):
            if count < dim:
                largest_length[count] = min(value, largest_length[count])

            else:
                largest_length[count] = max(value, largest_length[count])
    
    # minimal_position = list(local_goal)
    maximal_position = list(local_goal)
    orientation_position = list(local_goal)
    for count, value in enumerate(local_goal):
        up = upper_bounds[count] - value 
        down = value - lower_bounds[count]
        if up < down:
            orientation_position[count] = 1
            # minimal_position[count] = up
        else:
            orientation_position[count] = 0
    #         minimal_position[count] = down
    # minimal_position = np.array(minimal_position)
    # index_position = np.argmin(minimal_position)


    for index in range(dim):
        maximal_position[index] = largest_length[index + dim] - largest_length[index]
 
    maximal_position = np.array(maximal_position)
    index_position = np.argmax(maximal_position)

    if orientation_position[index_position] == 1:  # close to upper
        largest_length[index_position + dim] = largest_length[index_position] + size_box[index_position]
    else:
        largest_length[index_position] = largest_length[index_position + dim] - size_box[index_position]

    return largest_length



         

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
        system_file_name = "examples/traj_tracking.txt"
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



    # segment
    segment = 9
    TM.segment = segment

    base_name = f"{system}_traj_segm_{segment}_t{int(10*time)}_sb{subdiv_init}_ns{noise_level}"
    print(base_name)
    # local bounds used for compute MG
    region = TM.regions[TM.segment]
    dim = len(region)//2
    lower_bounds = region[0:dim]
    upper_bounds = region[dim:2*dim]
    local_goal = TM.local_goals[TM.segment]  # local_goals

    base_shift = region[0]
    pi = 3.14159
    shift = pi - base_shift


    shift_performed = False
    if region[0] > region[dim]:
        lower_bounds = transf(lower_bounds, shift)
        upper_bounds = transf(upper_bounds, shift)
        local_goal = transf(local_goal, shift)
        shift_performed = True

    print("REGION", region)
    print("BOUNDS", lower_bounds, upper_bounds)
    print("LOCAL GOAL", local_goal)

    # time
    TM.duration = time
    ### noise ###
    names_noise = ['xt', 'ft']
    parameters_upper_bounds = [TM.params["/plant/" + nname + "_noise_params"].as_float_vector()[1] for nname in names_noise]
    print(f"noise: xt & ft = {parameters_upper_bounds}")

    ### function ###
    if shift_performed:
        def g(X):
            X_temp = X[0::]
            X_temp = inv_transf(X_temp, shift)
            Y = TM.pendulum_trajectory_segment(X_temp)
            return transf(Y, shift)
    else:
        def g(X):
            return TM.pendulum_trajectory_segment(X)

    
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

    print(funnel(roa, lower_bounds, upper_bounds, local_goal))
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

        # base_name = "/output/" + base_name
        plt.savefig(base_name, bbox_inches='tight')
        plt.show()
