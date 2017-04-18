#!/bin/bash
#SBATCH -J HyWorkGPU
#SBATCH --array 0-100
#SBATCH -o logs/arr/gpu-%A_%a.out
#SBATCH -e logs/arr/gpu-%A_%a.err
#SBATCH --ntasks=1
#SBATCH --mail-type=end
#SBATCH --mail-user=1simon.pickert@mailbox.tu-dresden.de
#SBATCH --time=03:00:00
#SBATCH --ntasks=1
#SBATCH --output=logs/slurmStartWorkerArray.log
#SBATCH --mem=10000
sh HyperoptWorkerWrapper.sh $1