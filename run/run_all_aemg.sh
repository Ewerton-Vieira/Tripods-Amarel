cd /scratch/er691/TRIPODS-AMAREL/AEMG/run

dir_files=/scratch/er691/TRIPODS-AMAREL/AEMG/run
# cd ~/TRIPODS-AMAREL/AEMG/run

yourfilenames='ls /scratch/er691/TRIPODS-AMAREL/AEMG/run/*.sh'

for eachfile in $yourfilenames
do
    echo $(basename $eachfile)
    sbatch $(basename $eachfile)
done