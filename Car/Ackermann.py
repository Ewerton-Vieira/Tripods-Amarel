# Ackermann.py  # 2021-10-26
# MIT LICENSE 2020 Ewerton R. Vieira


import matplotlib
import matplotlib.pyplot as plt
import numpy as np
import math
import libpyDirtMP as prx
import csv
import time
import torch
import os
import CMGDB
from datetime import datetime
import time


class Ackermann:

    def __init__(self, ctrl_type="analytical", reverse=False, integration_step=0.01):
        """reverse = True: allow reverse movement"""

        # self.plant_name = "Ackermann_FO"
        # self.plant_path = "Ackermann_FO"
        #
        # self.car = prx.ackermann_FO(self.plant_name)
        #
        # self.wm = prx.world_model([self.car], [])
        # self.wm.create_context("context", [self.plant_name], [])
        # self.context = self.wm.get_context("context")
        #
        # self.start_state = self.context.system_group.get_state_space().make_point()
        # self.goal_state = self.context.system_group.get_state_space().make_point()
        #
        # self.eps = 0.1
        #
        # if ctrl_type == "analytical":
        #     self.lower_bounds = [-300, -300, -3.14159]
        #     self.upper_bounds = [300, 300, 3.14159]
        #
        #     self.lower_ctrl_bounds = [-1.05, 0]
        #     if reverse:
        #         self.lower_ctrl_bounds = [-1.05, -10]
        #
        #     self.upper_ctrl_bounds = [+1.05, 10]
        #
        # if ctrl_type != "analytical":
        #     self.lower_bounds = [-10, -10, -3.14159]
        #     self.upper_bounds = [10, 10, 3.14159]
        #     self.lower_bounds = [-5, -5, -3.14159]
        #     self.upper_bounds = [5, 5, 3.14159]
        #
        #     self.lower_ctrl_bounds = [-np.pi/3, 0]
        #     if reverse:
        #         self.lower_ctrl_bounds = [-np.pi/3, -30]
        #
        #     self.upper_ctrl_bounds = [+np.pi/3, 30]
        #
        #     # Provide the path to the controller
        #     path_to_model = "Ackermann_0_1.pt"
        #     self.controller = torch.load(path_to_model)
        #     # torch.manual_seed(111093)
        #     torch.manual_seed(11101993)
        #
        # self.context.system_group.get_state_space().set_bounds(self.lower_bounds, self.upper_bounds)
        #
        # self.checker = prx.condition_check("time", 0.1)
        #
        # self.cs = self.context.system_group.get_control_space()
        # self.cs.set_bounds(self.lower_ctrl_bounds, self.upper_ctrl_bounds)
        # self.ctrl_pt = self.cs.make_point
        #
        # prx.set_simulation_step(integration_step)

    def _enforce_bounds(self, s):
        while s[2] > np.pi:
            s[2] -= 2*np.pi
        while s[2] < -np.pi:
            s[2] += 2*np.pi
            s[2] = np.clip(s[2], -np.pi, np.pi)
        return s

    def goal_check(self, s, goal):
        diff = self._enforce_bounds(s-goal)
        return np.linalg.norm(diff) <= self.eps

    def G(self, X, step, propagation_step=0.01, goal_state_vec=[0, 0, 1.57]):

        # # best
        # k_rho = 1
        # k_alpha = 9.5
        # k_beta = -9.5

        # right
        # k_rho = 1
        # k_alpha = 9.5
        # k_beta = -4

        # # left
        # k_rho = 1
        # k_alpha = 4.5
        # k_beta = -19

        #  best controller so far
        if -1.9 <= X[0] and -1.8 <= X[1] <= 1.:
            k_rho = 1
            k_alpha = 9.5
            k_beta = -9.5
        else:
            k_rho = 1
            k_alpha = 9.5
            k_beta = -9

        self.car.set_gains(k_rho, k_alpha, k_beta)

        self.context.system_group.get_state_space().copy_point_from_vector(self.goal_state, goal_state_vec)

        start_state_vec = X
        self.context.system_group.get_state_space().copy_point_from_vector(self.start_state, start_state_vec)

        ss = self.context.system_group.get_state_space()
        state = ss.make_point()

        solution_traj = prx.trajectory(ss)
        ss.copy_from_point(self.start_state)
        ss.copy_point(state, self.start_state)

        # add this feature to assign the closest state to the goal
        # ss_closest_state = context.system_group.get_state_space()
        # closest_state = ss_closest_state.make_point()
        # ss_closest_state.copy_point(closest_state, start_state)

        i = 0
        while(i < step and prx.space_t.euclidean_2d(state, self.goal_state, 0, 3) > 0.01):

            solution_traj.copy_onto_back(state)
            self.car.compute_control(self.goal_state)

            self.cs.enforce_bounds()
            self.car.propagate(propagation_step)
            ss.copy_to_point(state)

            # add this feature to assign the closest state to the goal
            # if prx.space_t.euclidean_2d(state, goal_state, 0, 2) < prx.space_t.euclidean_2d(closest_state, goal_state, 0, 2):
            #     ss_closest_state.copy_point(closest_state, state)

            i += 1

        # add this feature to assign the closest state to the goal
        # return [closest_state[0], closest_state[1], closest_state[2]]
        return [state[0], state[1], state[2]]

    def G_check(self, f,  X, goal=[0, 0, 1.57]):
        Y = f(X)
        if np.linalg.norm(np.array(Y) - np.array(goal)) > 0.01:
            return [Y, False]
        else:
            return [Y, True]

    def G_2goals(X, step=1000, goal=[0, 0, 1.57]):
        Y = self.G(X, step, goal_state_vec=goal)
        if np.linalg.norm(np.array(Y) - np.array(goal)) > 0.01:
            Y_ = self.G(X, step, goal_state_vec=[4, 4, 1.57])
            Y = self.G(Y_, step, goal_state_vec=goal)
            if np.linalg.norm(np.array(Y) - np.array(goal)) > 0.01:
                return [Y, False]
            else:
                return [Y, True]
        else:
            return [Y, True]

    def G_learned(self, X, step, propagation_step=0.01, goal_state_vec=[0, 0, 1.57]):

        self.context.system_group.get_state_space().set_bounds(self.lower_bounds, self.upper_bounds)

        self.context.system_group.get_state_space().copy_point_from_vector(self.goal_state, goal_state_vec)

        start_state_vec = X
        self.context.system_group.get_state_space().copy_point_from_vector(self.start_state, start_state_vec)

        ss = self.context.system_group.get_state_space()
        state = ss.make_point()

        solution_traj = prx.trajectory(ss)
        ss.copy_from_point(self.start_state)
        ss.copy_point(state, self.start_state)

        current = np.zeros((3,))
        vec = np.zeros((6,))
        vec[0:3] = start_state_vec
        vec[3:6] = goal_state_vec

        i = 0

        # checker = prx.condition_check("time", 0.1)
        # while(not checker.check() and prx.space_t.euclidean_2d(state, goal_state, 0, 3) > 0.1):
        # while(i < step and self.goal_check(state, self.goal_state, 0, 3) > 0.1):
        while(i < step and not self.goal_check(vec[0:3], goal_state_vec)):
            # solution_traj.copy_onto_back(state)

            # ss.copy_vector_from_point(current,state

            # print("current:", current, "goal:", goal_state_vec)
            vec[0:3] = current = state
            vec[3:6] = goal_state_vec

            with torch.no_grad():
                controller_out = self.controller(torch.Tensor([vec]))[0].cpu()
            # print(controller_out)
            ctrl = np.array([-np.pi/3 + ((controller_out[0] + 1)*np.pi/3),
                             (controller_out[1]+1)*15])
            ctrl_l = ctrl.tolist()
            self.cs.copy_from_vector(ctrl_l)

            self.cs.enforce_bounds()
            self.car.propagate(propagation_step)
            vec[0:3] = state
            vec[0:3] = self._enforce_bounds(vec[0:3])
            self.context.system_group.get_state_space().copy_point_from_vector(state,
                                                                               [vec[0], vec[1], vec[2]])
            # ss.copy_point(state, vec[0:3])
            ss.copy_to_point(state)
            i += 1
            # vec[0:3] = state

        return [state[0], state[1], state[2]]

    def plot_data(self, X, Y, COLOR_X='r+', COLOR_Y='b.', LABEL_X='Initial points',
                  LABEL_Y='Endpoints', d=3, arrow=False, mixed_variables=False, name_graph="graph"):  # d = dimension
        fig = plt.figure(figsize=(9, 3))

        COLOR_ARROW = 'gray'  # 'lightgray'

        plt.subplot(1, 3, 1)
        d1 = 0
        d2 = 1
        plt.plot(X[:, d1], X[:, d2], COLOR_X, label=LABEL_X)
        plt.xlabel('x')
        plt.ylabel('y')
        plt.legend()
        # plt.grid()

        if arrow:
            for k in range(len(X[:, d1])):
                plt.arrow(X[:, d1][k], X[:, d2][k], np.cos(X[:, 2][k]),
                          np.sin(X[:, 2][k]), color=COLOR_ARROW)

        plt.subplot(1, 3, 2)
        plt.plot(Y[:, d1], Y[:, d2], COLOR_Y, label=LABEL_Y)
        # plt.xlabel('x[' + str(d1) +']');
        # plt.ylabel('x[' + str(d2) +']');
        plt.xlabel('x')
        plt.ylabel('y')
        plt.legend()
        # plt.grid()

        if arrow:
            for k in range(len(X[:, d1])):
                plt.arrow(Y[:, d1][k], Y[:, d2][k], np.cos(Y[:, 2][k]),
                          np.sin(Y[:, 2][k]), color=COLOR_ARROW)

        if d > 2:
            plt.subplot(1, 3, 3)
            d1 = 2
            d2 = 3
            plt.plot(X[:, 2], Y[:, 2], COLOR_X, label="theta")
            plt.legend()
            # plt.grid()
            # plt.xlabel('x[' + str(d1) +']');
            # plt.ylabel('x[' + str(d2) +']');
            plt.xlabel('theta_initial')
            plt.ylabel('theta_end')

            # Adjust spacing between subplots
            plt.subplots_adjust(hspace=0.2, wspace=0.3)
        # plt.show()
        plt.savefig(name_graph)

    def plot_graphs(self, f, x_cube=None, base_name="", save=False):
        """Plot graphs for function with success and fail
        f = function, x_cube = point in a cube
        base_name = base name for the files
        save = save files if True"""

        dir_path = os.path.abspath(os.getcwd()) + "/output/"

        y = []
        x_suc = []
        x_fail = []
        y_fail = []

        if type(x_cube) == type(None):

            with open(f, 'r') as file:
                lines = csv.reader(file, delimiter=' ')
                count_total = 0
                count_fail = 0
                for line in lines:
                    if line[6] == 'True':
                        y.append([float(a) for a in line[3:6]])
                        x_suc.append([float(a) for a in line[0:3]])
                    else:
                        y.append([float(a) for a in line[3:6]])
                        y_fail.append([float(a) for a in line[3:6]])
                        x_fail.append([float(a) for a in line[0:3]])
                        count_fail += 1
                    count_total += 1
                print(count_fail/count_total)

        else:
            for x_ in x_cube:
                y_ = self.G_check(f, x_)
                # print(x_, y_)
                # print(x_, f(x_))
                if y_[1]:
                    y.append(y_[0])
                    x_suc.append(x_)
                else:
                    y.append(y_[0])
                    y_fail.append(y_[0])
                    x_fail.append(x_)

        y = np.array(y)
        y_fail = np.array(y_fail)
        x_suc = np.array(x_suc)
        x_fail = np.array(x_fail)

        name_plot = dir_path + base_name + "_plots" + str(int(time.time()))
        if not type(x_cube) == type(None):
            self.plot_data(x_cube, y, arrow=True, name_graph=name_plot)
            plt.show()

            if save:
                plt.savefig(name_plot)

        if len(x_suc):
            # fig_s = plt.figure()
            # ax_s = fig_s.add_subplot(projection='3d')
            # ax_s.scatter(x_suc[:, 0], x_suc[:, 1], x_suc[:, 2])
            # ax_s.set_xlabel('X')
            # ax_s.set_ylabel('Y')
            # ax_s.set_zlabel('Z')
            # name_plot = dir_path + base_name + "_success3d" + str(int(time.time()))
            # if save:
            #     plt.savefig(name_plot)
            # plt.show()
            #
            # fig_s = plt.figure()
            # ax_s = fig_s.add_subplot()
            # ax_s.scatter(x_suc[:, 0], x_suc[:, 1])
            # ax_s.set_xlabel('X')
            # ax_s.set_ylabel('Y')
            # name_plot = dir_path + base_name + "_success2d" + str(int(time.time()))
            # if save:
            #     plt.savefig(name_plot)
            # plt.show()

            fig_f = plt.figure()
            ax_f = fig_f.add_subplot(projection='3d')
            ax_f.scatter(y[:, 0], y[:, 1], y[:, 2])
            ax_f.set_xlabel('X')
            ax_f.set_ylabel('Y')
            ax_f.set_zlabel('Z')
            name_plot = dir_path + base_name + "end_success3d" + str(int(time.time()))
            if save:
                plt.savefig(name_plot)
            plt.show()

        if len(x_fail):

            fig_f = plt.figure()
            ax_f = fig_f.add_subplot(projection='3d')
            ax_f.scatter(x_fail[:, 0], x_fail[:, 1], x_fail[:, 2])
            ax_f.set_xlabel('X')
            ax_f.set_ylabel('Y')
            ax_f.set_zlabel('Z')
            name_plot = dir_path + base_name + "initial_fail3d" + str(int(time.time()))
            if save:
                plt.savefig(name_plot)
            plt.show()

            fig_f = plt.figure()
            ax_f = fig_f.add_subplot(projection='3d')
            ax_f.scatter(y_fail[:, 0], y_fail[:, 1], y_fail[:, 2])
            ax_f.set_xlabel('X')
            ax_f.set_ylabel('Y')
            ax_f.set_zlabel('Z')
            name_plot = dir_path + base_name + "end_fail3d" + str(int(time.time()))
            if save:
                plt.savefig(name_plot)
            plt.show()

            fig_f = plt.figure()
            ax_f = fig_f.add_subplot()
            ax_f.scatter(x_fail[:, 0], x_fail[:, 1])
            ax_f.set_xlabel('X')
            ax_f.set_ylabel('Y')
            name_plot = dir_path + base_name + "initial_fail2d" + str(int(time.time()))
            if save:
                plt.savefig(name_plot)
            plt.show()


Ack = Ackermann()
Ack.plot_graphs("/Users/ewerton/Amarel/scratch/er691/Car/ackermann_lc_low_100_500.out",
                base_name='ackermann_60_1000_100_0_5', save=False)


# plot_graphs("ackermann_3.out", base_name='ackermann_3', save=False)

# Ack.plot_graphs("ackermann_100_50_50.out", base_name='ackermann_100_50_50', save=True)
# Ack.plot_graphs("ackermann_100_50_300.out", base_name='ackermann_100_50_300', save=True)
# Ack.plot_graphs("ackermann_100_150_50.out", base_name='ackermann_100_150_50', save=True)
# Ack.plot_graphs("ackermann_100_150_300.out", base_name='ackermann_100_150_300', save=True)
# Ack.plot_graphs("ackermann_100_150_300.out", base_name='ackermann_100_150_300', save=True)
# plot_graphs("ackermann_100_100_100_0_5.out", base_name='ackermann_100_100_100_0_5', save=True)
