#!/bin/bash

#SBATCH --job-name=Pen_lc_ns # Job name
#SBATCH --output=Pen_lc_ns%j.out     # STDOUT output file
#SBATCH --error=Pen_lc_ns%j.err      # STDERR output file (optional)
#SBATCH --partition=main      # Partition (job queue)
#SBATCH --nodes=1                     # Number of nodes
#SBATCH --ntasks=1                    # Total number of tasks across all nodes
#SBATCH --cpus-per-task=1             # Number of CPUs (cores) per task (>1 if multithread tasks)
#SBATCH --mem=32000                    # Real memory (RAM) required (MB)
#SBATCH --time=72:00:00               # Total run time limit (hh:mm:ss)
#SBATCH --requeue                     # Return job to the queue if preempted
#SBATCH --export=ALL                  # Export you current env to the job env

# Load necessary modules
#module purge
#module load python/3.5.2

cd /scratch/er691/Tripods-Amarel/

#  Run python script with input data
srun python compute_RoA.py examples/pendulum_lc_noise.txt