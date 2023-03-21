import argparse
import os


def exp_cluster(name_sh = "aemg.sh"):
    with open(name_sh, "r") as reader:
        halfs = reader.read().split("# split_here #")
    return halfs[0], halfs[1]




def main():

    parser = argparse.ArgumentParser()
    parser.add_argument('--run_dir',help='Directory of run files',type=str,default='run/')
    parser.add_argument('--config',help='Config file inside config_dir',type=str,default='discrete_map.txt')
    parser.add_argument('--name_out',help='Name of the out file',type=str,default='out_exp')

    args = parser.parse_args()
    

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
        '100_010_111',
        '100_010_11e1x',
        '100_010_11e2x',
        '100_010_e1x11',
        '100_010_e2x11',
        '100_010_0e1x1',
        '100_010_0e2x1',
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
    
    for _, exp_id in enumerate(exp_ids):
        name_file = f"run/{exp_id}.sh"

        with open(name_file, "w") as file:
            file.write(halfs_0)
            id = f"\nid=\'{exp_id}\'\n"
            file.write(id)
            file.write(halfs_1)

    


if __name__ == "__main__":
    main()