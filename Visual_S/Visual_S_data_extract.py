import sys
import os
import numpy as np


def sample_of_data(name_file, skip=1, time_step=2):
    """Read and embbed"""
    new_name = f"{name_file}_{skip}_{time_step}"
    with open(new_name, 'w') as new_file:

        with open(name_file, 'r') as file:

            k = 0
            while k < 1593185680:
            # while k < 11723:

                if not k % skip:
                    i = 0
                    line_input = str(file.readline())
                    line_input_list = line_input.split()
                    k += 1
                    if len(line_input_list)==7:

                        while i < time_step:
                            line_output = str(file.readline())
                            k += 1
                            if line_output == "\n" or "":
                                if i == 0:
                                    line_output_last = str(line_input)
                                break
                            i += 1
                            line_output_last = str(line_output)


                        line_output_list = line_output.split()

                        if len(line_output_list)==7:
                            new_file.writelines(line_input)
                            new_file.writelines(line_output)

                        else:
                            line_list = line_output_last.split()
                            if len(line_list)==7:
                                # x, y, z = float(line_list[0]), float(line_list[1]), float(line_list[2])
                                # r, p, yaw = float(line_list[3]), float(line_list[4]), float(line_list[5])
                                # if np.linalg.norm([x,y,z-0.75])<0.001 and np.linalg.norm([r,p,yaw])<0.02:
                                #     new_file.writelines(line_input)
                                #     new_file.writelines(line_output_last)
                                if int(line_list[6]) > 2:
                                    new_file.writelines(line_input)
                                    new_file.writelines(line_output_last)

                else:
                    k += 1
                    file.readline()


if __name__ == "__main__":

    system_file_name = "input_data.txt"

    with open(system_file_name, 'r') as f:
        config = eval(f.read())

    ######## Define the parameters ################
    sb = int(config['sb'])
    time = float(config['time'])  # propagation is 0.04
    noise_level = int(config['noise_level'])
    system = config['system']
    name_file = config['name_file']

    phase_periodic = [bool(a) for a in config['phase_periodic'].split()]
    K = [float(a) for a in config['K'].split()] # Lipschitz
    noise = [float(a) for a in config['noise'].split()] # global noise = [noise_x + noise_f + noise_u]*dim

    multivalued_map = config['multivalued_map']
    plot_RoA = int(config['plot_RoA'])

    skip = int(config['skip'])
    ######## Define the parameters ################

    dir_path = os.path.abspath(os.getcwd()) + "/data/"
    name_file = dir_path + name_file

    if len(sys.argv) > 2:
        time = float(sys.argv[1])
        skip = int(sys.argv[2])

    time_step = int(np.around(time / 0.04))



    sample_of_data(name_file, skip=skip, time_step=time_step)
