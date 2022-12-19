import sys
import os


def sample_of_data(name_file, skip=1, time_step=2):
    """Read and embbed"""
    new_name = f"{name_file}_{skip}_{time_step}"
    with open(new_name, 'w') as new_file:

        with open(name_file, 'r') as file:

            k = 0
            while k < 1593185680:
            # while k < 50:

                if not k % skip:
                    i = 0
                    line_input = str(file.readline())
                    k += 1
                    if line_input != "\n":

                        while i < time_step:
                            line_output = str(file.readline())
                            k += 1
                            if line_output == "\n":
                                break
                            i += 1

                        if line_output != '\n' and line_output != '':

                            new_file.writelines(line_input)
                            new_file.writelines(line_output)
                        # else:
                        #     new_file.writelines("\n")

                    # else:
                    #     new_file.writelines("\n")

                else:
                    k += 1
                    file.readline()


if __name__ == "__main__":

    name_file = "data_vs"
    # name_file = "test.txt"

    dir_path = os.path.abspath(os.getcwd()) + "/data/"
    name_file = dir_path + name_file
    sample_of_data(name_file, skip=1, time_step=4)
