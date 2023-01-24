#!/bin/bash

#SBATCH --job-name=Data_ex # Job name
#SBATCH --output=Data_ex%j.out     # STDOUT output file
#SBATCH --error=Data_ex%j.err      # STDERR output file (optional)
#SBATCH --partition=p_mischaik_1     # Partition (job queue)
#SBATCH --nodes=1                     # Number of nodes
#SBATCH --ntasks=1                    # Total number of tasks across all nodes
#SBATCH --cpus-per-task=1             # Number of CPUs (cores) per task (>1 if multithread tasks)
#SBATCH --mem=12000                    # Real memory (RAM) required (MB)
#SBATCH --time=24:00:00               # Total run time limit (hh:mm:ss)
#SBATCH --requeue                     # Return job to the queue if preempted
#SBATCH --export=ALL                  # Export you current env to the job env

# Load necessary modules
#module purge
#module load python/3.5.2

cd /scratch/er691/Tripods-Amarel/Visual_S/

#  Run python script with input data
srun python Visual_S_data_extract.py
