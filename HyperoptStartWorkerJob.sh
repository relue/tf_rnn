#!/bin/bash
#SBATCH --output=logs/SlurmHyperoptStartWorkers.log
#SBATCH --ntasks=1
#SBATCH --mem=15000
#SBATCH --time=24:00:00
#SBATCH --job-name=startJobs
srun --time=02:00:00 --mem=15000 ~/pythonProjects/env/bin/python2.7 -W ignore HyperoptStartWorkers.py
