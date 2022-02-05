import numpy as np
from datetime import datetime
import TimeMap
import Grid


sb = 20
time = 16  # time in seconds
time_lc = 5
time_lqr = 11

MG_util = CMGDB_util.CMGDB_util()

subdiv_init = subdiv_min = subdiv_max = sb  # non adaptive proceedure

# POSITION_BOUNDS
EPSILON_THETAS = pi = 3.141592653589793  # size of the box with the center at the goal (thetas)
EPSILON_DOTS = 6  # 6  # size of the box with the center at the goal (thetas_dot)

tau = 14  # bounds on torque


lower_bounds = [-EPSILON_THETAS + pi, -EPSILON_THETAS, -EPSILON_DOTS, -EPSILON_DOTS]
upper_bounds = [EPSILON_THETAS + pi, EPSILON_THETAS, EPSILON_DOTS, EPSILON_DOTS]

# base name for the output files.
base_name = "Acrobot_hyb_time" + str(time) + "_torque" + str(tau) + "_" + str(subdiv_init)

print(base_name)

TM_lqr = TimeMap.TimeMap("acrobot_lqr", time_lqr, "examples/tripods/acrobot_roa.yaml")
TM_lc = TimeMap.TimeMap("acrobot_lc", time_lc, "examples/tripods/acrobot_lc.yaml")


def g(X):
    output_of_lc = TM_lc.acrobot_lc(X)
    # print(output_of_lc)
    return TM_lqr.acrobot_lqr(output_of_lc)


# Grid
grid = Grid.Grid(lower_bounds, upper_bounds, sb, base_name=base_name)

startTime = datetime.now()
grid.write_map_grid(g, lower_bounds, upper_bounds, sb, base_name=base_name)
print(f"Time to save map_grid = {datetime.now() - startTime}")
