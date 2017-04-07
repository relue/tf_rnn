#!/bin/bash
#SBATCH --output=slurmStartWorker.log
#SBATCH --ntasks=1
#SBATCH --mem=10000
srun --time=02:00:00 ~/pythonProjects/env/bin/python2.7 -W ignore ~/pythonProjects/tf_rnn/HyperoptWorkerWrapper.py 192.168.234.129