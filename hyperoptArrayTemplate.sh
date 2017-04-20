#!/bin/bash
#SBATCH -J HyWorkers
#SBATCH --array 0-3500
#SBATCH -o logs/arr/cpu-%a.out
#SBATCH -e logs/arr/cpu-%a.err
#SBATCH --ntasks=1
#SBATCH --time=07:00:00
#SBATCH --mem-per-cpu=2500
sh HyperoptWorkerWrapper.sh $1
