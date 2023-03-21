#!/bin/bash

#SBATCH --job-name=AEMG # Job name
#SBATCH --output=AEMG%j.out     # STDOUT output file
#SBATCH --error=AEMG%j.err      # STDERR output file (optional)
#SBATCH --partition=p_mischaik_1      # Partition (job queue)
#SBATCH --nodes=1                     # Number of nodes
#SBATCH --ntasks=1                    # Total number of tasks across all nodes
#SBATCH --cpus-per-task=1             # Number of CPUs (cores) per task (>1 if multithread tasks)
#SBATCH --mem=1000                    # Real memory (RAM) required (MB)
#SBATCH --time=72:00:00               # Total run time limit (hh:mm:ss)
#SBATCH --requeue                     # Return job to the queue if preempted
#SBATCH --export=ALL                  # Export you current env to the job env

# Load necessary modules
#module purge
#module load python/3.8.5

cd /scratch/er691/AEMG/examples

#  Run python script with input data

id='100_010_0e1x1'


search_dir=config/exp_bistable_1k/$id/

yourfilenames=`ls $(pwd)/$search_dir*.txt`

for eachfile in $yourfilenames
do
    echo $(basename $eachfile)
    python train.py --config_dir "$search_dir" --config "$(basename $eachfile)" --print_out 0
    python get_MG_RoA.py --config_dir "$search_dir" --config "$(basename $eachfile)" --name_out "$id"
done
