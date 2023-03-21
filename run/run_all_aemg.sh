cd /scratch/er691/TRIPODS-AMAREL/AEMG/run

# cd ~/TRIPODS-AMAREL/AEMG/run

yourfilenames='ls $(pwd)/*.sh'

for eachfile in $yourfilenames
do
    echo $(basename $eachfile)
    sbatch $(basename $eachfile)
done