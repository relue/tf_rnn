#!/bin/bash
#SBATCH --output=logs/slurmStartWorker.log
#SBATCH --ntasks=1
#SBATCH --mem=10000
srun --ntasks=1 --time=01:00:00 --mem=10000 sh ~/pythonProjects/tf_rnn/HyperoptWorkerWrapper.sh 127
