#!/bin/bash
#SBATCH -J HyWorkers
#SBATCH --array 0-3500
#SBATCH -o logs/arr/cpu-%a.out
#SBATCH -e logs/arr/cpu-%a.err
#SBATCH --ntasks=1
#SBATCH --mail-type=end
#SBATCH --mail-user=1simon.pickert@mailbox.tu-dresden.de
#SBATCH --time=06:00:00
#SBATCH --mem-per-cpu=2500
sh HyperoptWorkerWrapper.sh $1
