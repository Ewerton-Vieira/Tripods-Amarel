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
                    if line_input != "\n" and len(line_input_list)==7:

                        while i < time_step:
                            line_output = str(file.readline())
                            k += 1
                            if line_output == "\n":
                                if i = 0:
                                    line_output_last = ""
                                break
                            i += 1
                            line_output_last = str(line_output)


                        line_output_list = line_output.split()

                        if line_output != '\n' and line_output != '' and len(line_output_list)==7:
                            new_file.writelines(line_input)
                            new_file.writelines(line_output)

                        else:
                            if line_output_last != '\n' and line_output_last != '':
                                line_list = line_output_last.split()
                                x, y, z = float(line_list[0]), float(line_list[1]), float(line_list[2])
                                r, p, yaw = float(line_list[3]), float(line_list[4]), float(line_list[5])

                                if np.linalg.norm([x,y,z-0.75])<0.001 and np.linalg.norm([r,p,yaw])<0.02 and line_list == 7:
                                    new_file.writelines(line_input)
                                    new_file.writelines(line_output_last)

                else:
                    k += 1
                    file.readline()


if __name__ == "__main__":

    name_file = "data_vs"
    # name_file = "test.txt"

    dir_path = os.path.abspath(os.getcwd()) + "/data/"
    name_file = dir_path + name_file
    sample_of_data(name_file, skip=20, time_step=30)
