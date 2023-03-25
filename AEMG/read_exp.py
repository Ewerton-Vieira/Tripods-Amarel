import os


def read_write_old(file_out, file2read):

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

def main():

    dir_source = "/scratch/er691/AEMG/examples/output"
    # dir_source = "/Users/ewerton/Dropbox/Codes/AEMG/examples/output"

    dict_write=dict()


    for a in ["","0","00"]:
        dir_temp = f"{dir_source}/bistable1{a}k"
            
        for b in os.listdir(dir_temp):
            file2read = os.path.join(dir_temp, b)
            temp = ''
            count = 0
            total = 0

            with open(file2read, "r") as reader:
                line = reader.readline()
                line_split = line.split(",")

                while line != '':
                    key = line_split[0]
                    if key not in dict_write:
                        dict_write[key] = line_split[1]              
                    else:
                        dict_write[key] += line_split[1]
                    
                    line = reader.readline()
                    line_split = line.split(",")
                    
    with open("out_exp.txt", "w") as file_out:
        for key, value in dict_write.items():
            file_out.write(key)
            total = len(value)
            success = value.count("1")
            a = f",{total},{success},{success/total}\n"
            file_out.write(a)


if __name__ == "__main__":
    main()