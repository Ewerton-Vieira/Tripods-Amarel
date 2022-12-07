## Amarel commands


# Amarel custer
ssh er691@amarel.rutgers.edu

# Move file to Amarel
scp run.sh er691@amarel.rutgers.edu:/home/er691/

scp FILE_NAME er691@amarel.rutgers.edu:/scratch/er691/Car/

scp Car.py er691@amarel.rutgers.edu:/scratch/er691/Car/

scp car_unidirection.py er691@amarel.rutgers.edu:/scratch/er691/Car/

scp car_L.py er691@amarel.rutgers.edu:/scratch/er691/Car/

scp ai_car.py er691@amarel.rutgers.edu:/scratch/er691/Car/

scp ai_car_L.py er691@amarel.rutgers.edu:/scratch/er691/Car/

scp car_inf.py er691@amarel.rutgers.edu:/scratch/er691/Car/

scp car_inf_K10.py er691@amarel.rutgers.edu:/scratch/er691/Car/

scp car2dyn.py er691@amarel.rutgers.edu:/scratch/er691/Car/

scp GP_Amarel.py er691@amarel.rutgers.edu:/scratch/er691/

scp Car_step1000_20_30.csv er691@amarel.rutgers.edu:/scratch/er691/3d/

scp /Users/ewerton/Dropbox/Codes/Amarel/toSend/1.tgz er691@amarel.rutgers.edu:/scratch/er691/

scp /Users/ewerton/Dropbox/Codes/Amarel/toSend/DirtMP_step1000_torque7_30_40.py er691@amarel.rutgers.edu:/scratch/er691/

# Get file from Amarel

scp er691@amarel.rutgers.edu:/scratch/er691/er691.tar.gz ~/Dropbox/Codes/Amarel/

scp er691@amarel.rutgers.edu:/home/er691/CMGDB/morse.csv .

scp er691@amarel.rutgers.edu:/scratch/er691/SingleCMG_statistics.txt .

scp er691@amarel.rutgers.edu:/scratch/er691/morse_sets_GP_Amarel.csv .

# zip folder and sent it

tar -zcvf /scratch/er691/er691.tar.gz /scratch/er691/

scp er691@amarel.rutgers.edu:/scratch/er691/er691.tar.gz ~/Dropbox/Codes/Amarel/

# interative job
srun --mem=8000 --time=24:30:00 --pty bash

# batch
sbatch run3d.sh

# check job list
squeue -u er691

## Bash commands

# bash profile
nano ~/.bashrc

# rename or move
mv <source_directory> <target_directory>

# remove
rm file_1.txt

# compress folder
tar -czvf NAME_OF_FILE.tgz FOLDER_NAME

    # keep path not good
tar -czvf /Users/ewerton/Dropbox/Codes/Amarel/toSend/1.tgz /Users/ewerton/Dropbox/Codes/Amarel/toSend

tar -czvf 1.tgz /Users/ewerton/Dropbox/Codes/Amarel/toSend
    # keep path not good

    # use this
tar -czvf 1.tgz .

# unzip folder

tar -xvf 1.tgz

# ipy to py

jupyter nbconvert --to python GP_Amarel.ipynb

jupyter nbconvert --to python DirtMP_step1000_torque7_30_40.ipynb
jupyter nbconvert --to python 2.ipynb


https://rutgers.box.com/s/51fam19pd8gkahj96xgg71vzn28tdzqp
