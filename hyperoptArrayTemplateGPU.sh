#!/bin/bash
#SBATCH -J HyWorkGPU
#SBATCH --array 0-2000
#SBATCH -o logs/arr/gpu-%a.out
#SBATCH -e logs/arr/gpu-%a.err
#SBATCH --ntasks=1
#SBATCH --mail-type=end
#SBATCH --mail-user=1simon.pickert@mailbox.tu-dresden.de
#SBATCH --time=12:00:00
#SBATCH --mem=10000
#SBATCH --gres=gpu:1
sh HyperoptWorkerWrapper.sh $1