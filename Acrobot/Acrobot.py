import sys
import math
import random
# Remember to add libpyDirtMP to your PYTHONPATH
# On bash: ``export PYTHONPATH=$DIRTMP_PATH/lib/:$PYTHONPATH
import libpyDirtMP as prx

import matplotlib
import matplotlib.pyplot as plt
import numpy as np


params = prx.param_loader("examples/intermediate/lqr.yaml", sys.argv)

prx.set_simulation_step(params["simulation_step"].as_float())
prx.init_random(params["random_seed"].as_int())

# Could be done directly from params, calling the getter to show that is there...
simulation_step = prx.get_simulation_step()
# Safety check
print("simulation_step:", simulation_step)

obstacles = prx.load_obstacles(params["environment"].as_string())
obstacle_list = obstacles.objects
obstacle_names = obstacles.names

plant_name = params["/plant/name"].as_string()
plant_path = params["/plant/path"].as_string()
plant = prx.system_factory.create_system(plant_name, plant_path)
# plant = prx.pendulum(plant_name, plant_path)
# prx_assert(plant != nullptr, "Plant is nullptr!");
if plant == None:
    print("Error: plant not found!")
    exit(-1)

wm = prx.world_model([plant], obstacle_list)
wm.create_context("context", [plant_name], obstacle_names)
context = wm.get_context("context")

ss = context.system_group.get_state_space()
cs = context.system_group.get_control_space()

lower_bounds = params["/plant/state_space_lower_bound"].as_float_vector()
upper_bounds = params["/plant/state_space_upper_bound"].as_float_vector()
ss.set_bounds(lower_bounds, upper_bounds)

cs_lb = params["/plant/control_space_lower_bound"].as_float_vector()
cs_up = params["/plant/control_space_upper_bound"].as_float_vector()
cs.set_bounds(cs_lb, cs_up)

start_state = ss.make_point()
goal_state = ss.make_point()

ss.copy_point_from_vector(start_state, params["/plant/start_state"].as_float_vector())
ss.copy_point_from_vector(goal_state, params["/plant/goal_state"].as_float_vector())
ss.copy_from_point(start_state)

checker = prx.condition_check(
    params["checker_type"].as_string(), params["checker_value"].as_int())

solution_traj = prx.trajectory(ss)
solution_traj.copy_onto_back(ss)

plant.linearize()

ss_dim = ss.get_dimension()
cs_dim = cs.get_dimension()

Q = prx.matrix.Identity(ss_dim, ss_dim)
q_vec = params["/plant/lqr_Q"].as_float_vector()
# Using the type matrix, but really is a vector
v_goal = prx.vector.Zero(ss_dim)
# v_goal = prx.matrix.Zero(ss_dim, 1);
for i in range(ss_dim):
    Q[i, i] = q_vec[i]
    v_goal[i] = goal_state[i]
print("Q:", Q)
R = prx.matrix.Identity(cs_dim, cs_dim)
R[0, 0] = 1
# ss.copy_vector_from_point(v_goal, goal_state);
print("goal_state:", goal_state)
print("v_goal:", v_goal)

lqr = prx.lqr(plant, Q, R, "LQR")
lqr.set_goal(v_goal)
lqr.compute_K()
K = lqr.get_K()
print("K: ", K)


BOUNDS_ON_DOTS = 6
ssmin = [0, -np.pi, -BOUNDS_ON_DOTS, -BOUNDS_ON_DOTS]
ssmax = [2 * np.pi, np.pi, BOUNDS_ON_DOTS, BOUNDS_ON_DOTS]

ss.set_bounds(ssmin, ssmax)

ss_pt_aux = ss.make_point()


def G(X, tau, step, int_step=0.01):

    # Now, we can copy directly a python list/vector to a space
    ss.copy_from_vector(X)
    # Using python lists directly
    cs_lb = [-tau]
    cs_ub = [tau]

    # Assign bound to the space. Internally, it checks that the dimensions
    # of the space and the list are the same, throwing an error if not.

    cs.set_bounds(cs_lb, cs_up)

    # print("control \\in", cs.get_lower_bounds(), cs.get_upper_bounds())
    # print("state \\in", ss.get_lower_bounds(), ss.get_upper_bounds())
    # construct to auxiliary points. This are not strictly necessary...

    # This is ok, but it might be better to use the condition_checker
    # with a while true: (...) => if checker.check(): break
    for i in range(step):
        # before it was: acrobot.apply_lqr()
        lqr.compute_controls()
        # Redundant, this is already called internally but for safety is ok
        # cs.enforce_bounds()
        # Same as before
        plant.propagate(int_step)

    ss.copy_to_point(ss_pt_aux)
    # Return a list with the last state of the plant
    return [ss_pt_aux[0], ss_pt_aux[1], ss_pt_aux[2], ss_pt_aux[3]]


def plot_orbit(X, tau, step):
    x = [X]
    for i in range(step):
        x.append(G(x[len(x) - 1], tau, 1))
    x = np.array(x)
    plt.figure()
    ax = plt.subplot(121)
    # ax.plot([2, 2, 4], [0, 1, 3])
    ax.plot(x[:, 0], x[:, 1])
    ax.plot(x[:, 0][0], x[:, 1][0], "or")
    ax.plot(x[:, 0][-1], x[:, 1][-1], "ok")
    ax = plt.subplot(122)
    ax.plot(x[:, 2], x[:, 3])
    ax.plot(x[:, 2][0], x[:, 3][0], "or")
    ax.plot(x[:, 2][-1], x[:, 3][-1], "ok")
    # ax = plt.subplot(223)
    # ax.plot(2, 1)
    # ax = plt.subplot(224)
    # ax.plot(2, 1)

    return x


def sample_points(lower_bounds, upper_bounds, num_pts):
    # Sample num_pts in dimension dim, where each
    # component of the sampled points are in the
    # ranges given by lower_bounds and upper_bounds
    dim = len(lower_bounds)
    X = np.random.uniform(lower_bounds, upper_bounds, size=(num_pts, dim))
    return X


def plot_data(X, Y, COLOR_X='ro', COLOR_Y='bx', LABEL_X='Initial points', LABEL_Y='Endpoints', d=4, arrow=False, mixed_variables=False):  # d = dimension
    fig = plt.figure(figsize=(10, 10))

    COLOR_ARROW = 'lightgray'

    plt.subplot(2, 2, 1)
    d1 = 0
    d2 = 1
    plt.plot(X[:, d1], X[:, d2], COLOR_X, label=LABEL_X)
    plt.plot(Y[:, d1], Y[:, d2], COLOR_Y, label=LABEL_Y)
    # plt.xlabel('x[' + str(d1) +']');
    # plt.ylabel('x[' + str(d2) +']');
    plt.xlabel('theta 1')
    plt.ylabel('theta 2')
    plt.legend()
    # plt.grid()

    if arrow:
        for k in range(len(X[:, d1])):
            plt.arrow(X[:, d1][k], X[:, d2][k], Y[:, d1][k] -
                      X[:, d1][k], Y[:, d2][k] - X[:, d2][k], color=COLOR_ARROW)

    if d > 2:
        plt.subplot(2, 2, 2)
        d1 = 2
        d2 = 3
        plt.plot(X[:, d1], X[:, d2], COLOR_X, label=LABEL_X)
        plt.plot(Y[:, d1], Y[:, d2], COLOR_Y, label=LABEL_Y)
        plt.legend()
        # plt.grid()
        # plt.xlabel('x[' + str(d1) +']');
        # plt.ylabel('x[' + str(d2) +']');
        plt.xlabel('theta_dot 1')
        plt.ylabel('theta_dot 2')
        if arrow:
            for k in range(len(X[:, d1])):
                plt.arrow(X[:, d1][k], X[:, d2][k], Y[:, d1][k] -
                          X[:, d1][k], Y[:, d2][k] - X[:, d2][k], color=COLOR_ARROW)

        if mixed_variables:

            plt.subplot(2, 2, 3)
            d1 = 0
            d2 = 2
            plt.plot(X[:, d1], X[:, d2], COLOR_X, label=LABEL_X)
            plt.plot(Y[:, d1], Y[:, d2], COLOR_Y, label=LABEL_Y)
            plt.legend()
            # plt.grid()
            # plt.xlabel('x[' + str(d1) +']');
            # plt.ylabel('x[' + str(d2) +']');
            plt.xlabel('theta 1')
            plt.ylabel('theta_dot 1')
            if arrow:
                for k in range(len(X[:, d1])):
                    plt.arrow(X[:, d1][k], X[:, d2][k], Y[:, d1][k] -
                              X[:, d1][k], Y[:, d2][k] - X[:, d2][k], color=COLOR_ARROW)

            plt.subplot(2, 2, 4)
            d1 = 1
            d2 = 3
            plt.plot(X[:, d1], X[:, d2], COLOR_X, label=LABEL_X)
            plt.plot(Y[:, d1], Y[:, d2], COLOR_Y, label=LABEL_Y)
            plt.legend()
            # plt.grid()
            # plt.xlabel('x[' + str(d1) +']');
            # plt.ylabel('x[' + str(d2) +']');
            plt.xlabel('theta 2')
            plt.ylabel('theta_dot 2')
            if arrow:
                for k in range(len(X[:, d1])):
                    plt.arrow(X[:, d1][k], X[:, d2][k], Y[:, d1][k] -
                              X[:, d1][k], Y[:, d2][k] - X[:, d2][k], color=COLOR_ARROW)

        # Adjust spacing between subplots
        plt.subplots_adjust(hspace=0.2, wspace=0.3)
    plt.show()


def draw_path(PATH='Data/state_0.txt', STEP=1, PERIODIC=False):
    STEP_DATA = 0.01  # time step in data
    path_x, path_y = read_files([PATH], STEP)

    if PERIODIC:
        for j in range(2):
            path_x[:, j] = np.cos(path_x[:, j])

    STEP_LIST = [a * STEP * STEP_DATA for a in range(len(path_x[:, 0]))]

    fig, ax = plt.subplots(2, 2, figsize=(10, 10))
    fig.subplots_adjust(wspace=0.6)

    ax[0, 0].plot(STEP_LIST, path_x[:, 0])
    ax[0, 0].set_xlabel("time")
    ax[0, 0].set_ylabel("theta1")

    ax[0, 1].plot(STEP_LIST, path_x[:, 1])
    ax[0, 1].set_xlabel("time")
    ax[0, 1].set_ylabel("theta2")

    ax[1, 0].plot(STEP_LIST, path_x[:, 2])
    ax[1, 0].set_xlabel("time")
    ax[1, 0].set_ylabel("dot_theta1")

    ax[1, 1].plot(STEP_LIST, path_x[:, 3])
    ax[1, 1].set_xlabel("time")
    ax[1, 1].set_ylabel("dot_theta2")
    plt.show()
    fig.savefig('fig.png')
