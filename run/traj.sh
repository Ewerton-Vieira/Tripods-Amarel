#!/bin/bash

#SBATCH --job-name=Traj_full_RoA # Job name
#SBATCH --output=Traj_full_RoA%j.out     # STDOUT output file
#SBATCH --error=Vs_RoA%j.err      # STDERR output file (optional)
#SBATCH --partition=p_mischaik_1      # Partition (job queue)
#SBATCH --nodes=1                     # Number of nodes
#SBATCH --ntasks=1                    # Total number of tasks across all nodes
#SBATCH --cpus-per-task=1             # Number of CPUs (cores) per task (>1 if multithread tasks)
#SBATCH --mem=64000                    # Real memory (RAM) required (MB)
#SBATCH --time=8:00:00               # Total run time limit (hh:mm:ss)
#SBATCH --requeue                     # Return job to the queue if preempted
#SBATCH --export=ALL                  # Export you current env to the job env

# Load necessary modules
#module purge
#module load python/3.5.2

cd /scratch/er691/Tripods-Amarel/


srun python traj_full_RoA.py
