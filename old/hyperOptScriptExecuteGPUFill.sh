#!/bin/bash
#SBATCH --output=logs/slurmStartWorkerGPU.log
#SBATCH --mem=10000
#SBATCH --gres=gpu:1
srun --gres=gpu:1 --time=01:00:00 --mem=10000 sh ~/pythonProjects/tf_rnn/HyperoptWorkerWrapper.sh 127
