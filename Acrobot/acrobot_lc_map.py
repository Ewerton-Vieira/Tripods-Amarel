import numpy as np
from datetime import datetime
import TimeMap
import Grid


sb = 20
time = 5  # time in seconds

MG_util = CMGDB_util.CMGDB_util()

subdiv_init = subdiv_min = subdiv_max = sb  # non adaptive proceedure

# POSITION_BOUNDS
EPSILON_THETAS = pi = 3.141592653589793  # size of the box with the center at the goal (thetas)
EPSILON_DOTS = 6  # 6  # size of the box with the center at the goal (thetas_dot)

tau = 14  # bounds on torque


lower_bounds = [-EPSILON_THETAS + pi, -EPSILON_THETAS, -EPSILON_DOTS, -EPSILON_DOTS]
upper_bounds = [EPSILON_THETAS + pi, EPSILON_THETAS, EPSILON_DOTS, EPSILON_DOTS]

# base name for the output files.
base_name = "Acrobot_lc_time" + str(time) + "_torque" + str(tau) + \
    "_" + str(subdiv_init) + "_map_grid"

print(base_name)


TM = TimeMap.TimeMap("acrobot_lc", time,
                     "examples/tripods/acrobot_lc.yaml")


def g(X):
    return TM.acrobot_lc(X)


# Grid
grid = Grid.Grid(lower_bounds, upper_bounds, sb, base_name=base_name)

startTime = datetime.now()
grid.write_map_grid(g, lower_bounds, upper_bounds, sb, base_name=base_name)
print(f"Time to save map_grid = {datetime.now() - startTime}")
