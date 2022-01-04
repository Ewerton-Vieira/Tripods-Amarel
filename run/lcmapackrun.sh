#!/bin/bash

#SBATCH --job-name=Lc_ack_MG # Job name
#SBATCH --output=Lc_ack_output_%N_%j.out     # STDOUT output file
#SBATCH --error=Lc_ack_output_%N_%j.err      # STDERR output file (optional)
#SBATCH --partition=main              # Partition (job queue)
#SBATCH --nodes=1                     # Number of nodes
#SBATCH --ntasks=1                    # Total number of tasks across all nodes
#SBATCH --cpus-per-task=4             # Number of CPUs (cores) per task (>1 if multithread tasks)
#SBATCH --mem=128000                    # Real memory (RAM) required (MB)
#SBATCH --time=48:00:00               # Total run time limit (hh:mm:ss)
#SBATCH --requeue                     # Return job to the queue if preempted
#SBATCH --export=ALL                  # Export you current env to the job env

# Load necessary modules
#module purge
#module load python/3.5.2

cd /scratch/er691/Tripods-Amarel/Car

#  Run python script with input data
srun python ackermann_lc_map.py
