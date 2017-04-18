#!/bin/bash
#SBATCH --output=logs/slurmStartWorker.log
#SBATCH --ntasks=1
#SBATCH --mem=10000
#srun --time=12:00:00 --mem=10000 ~/pythonProjects/env/bin/python2.7 -W ignore ~/pythonProjects/tf_rnn/hyperoptSpamWorkers.py 192.168.221.253
