import os

def main():

    dir_source = "/scratch/er691/AEMG/examples/output"

    with open("out_exp", "w") as file_out:
        for a in ["","0","00"]:
            dir_temp = f"{dir_source}/bistable1{a}k"
             
            for b in os.listdir(dir_temp):
                dir_temp2 = os.path.join(dir_temp, b)
                for temp_path in os.listdir(dir_temp2):
                    temp = ''
                    count = 0
                    total = 0

                    file2read = os.path.join(dir_temp2, temp_path)

                    with open(file2read, "r") as reader:

                        line = reader.readline()
                        line_split = line.split(",")
                        file_out.write(line_split[0])

                        temp = str(line_split[0])

                        while True:
                            if line_split[0] != temp:
                                a = f",{count},{total},{total/count}\n"
                                file_out.write(a)
                                if line == "":
                                    break
                                file_out.write(line_split[0])
                                total = int(line_split[1])
                                count = 0
                            else:
                                total += int(line_split[1])

                            count += 1
                            temp = str(line_split[0])

                            line = reader.readline()
                            line_split = line.split(",")


if __name__ == "__main__":
    main()