import argparse
import os


def exp_cluster(name_sh = "aemg.sh"):
    with open(name_sh, "r") as reader:
        halfs = reader.read().split("# split_here #")
    return halfs[0], halfs[1]




def main():

    parser = argparse.ArgumentParser()
    parser.add_argument('--run_dir',help='Directory of run files',type=str,default='run/bistable1k')
    parser.add_argument('--config',help='Config file inside config_dir',type=str,default='discrete_map.txt')
    parser.add_argument('--name_out',help='Name of the out file',type=str,default='out_exp')
    parser.add_argument('--system',help='Name of the system',type=str,default='discrete_map')
    parser.add_argument('--control',help='Name of the control',type=str,default='bistable')

    args = parser.parse_args()

    args.run_dir = os.path.join(os.getcwd(), args.run_dir)
    

    if not os.path.exists(args.run_dir):
        os.makedirs(args.run_dir)

    exp_ids = [
        '111',
        '11e1x',
        '11e2x',
        '11e3x',
        'e1x11',
        'e2x11',
        'e3x11',
        '1e1x1',
        '1e2x1',
        '1e3x1',
        '100_111',
        '100_e1_11',
        '100_1e1x1',
        '100_11e1x',
        '100_011x111',
        '100_011_111',
        '100_011_11e1x',
        '100_011_11e2x',
        '100_011_e1x11',
        '100_011_e2x11',
        '100_011_111',
        '100_011_11e1x',
        '100_011_11e2x',
        '100_011_e1x11',
        '100_011_e2x11',
        '100_001_010_111',
        '100_001_010_11e1x',
        '100_001_010_11e2x',
        '100_001_010_e1x11',
        '100_001_010_e2x11',
        '100_001_010_1e1x1',
        '100_001_010_1e2x1',
        '100_001_010_1e1xe1x',
        '100_001_010_1e2xe2x',
        '100_001_010_e1x1e1x',
        '100_001_010_e2x1e2x',
        '100_001_010_e1xe1x1',
        '100_001_010_e1xe2x1',
        '100_001_110_001',
        '100_001_e1x10_001',
        '100_001_e2x10_001',
        '100_001_1e1x0_001',
        '100_001_1e2x0_001',
        '100_001_110_001_111',
        '100_001_e1x10_001_111',
        '100_001_e2x10_001_111',
        '100_001_1e1x0_001_111',
        '100_001_1e2x0_001_111',
        '100_001_110_001_11e1x',
        '100_001_110_001_11e2x',
        '100_001_110_001_1e1x1',
        '100_001_110_001_1e2x1',
        '100_001_110_001_e1x11',
        '100_001_110_001_e2x11',
        # Feel free to add more here
    ]

    halfs_0, halfs_1 = exp_cluster(name_sh = "aemg.sh")

    with open("sample_run", 'w') as sample:
    
        for _, exp_id in enumerate(exp_ids):
            name_file = f"{args.run_dir}/{exp_id}.sh"

            with open(name_file, "w") as file:
                file.write(halfs_0)

                id = f"\nid=\'{exp_id}\'\n"
                file.write(id)

                system_control_k=f"\nsystem_control_k={args.system}_{args.control}k\n"
                file.write(system_control_k)

                file.write(halfs_1)

            sample.writelines(f"sbatch {exp_id}.sh\n")

    


if __name__ == "__main__":
    main()