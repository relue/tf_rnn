#!/bin/bash
#SBATCH --output=logs/SlurmHyperoptStartWorkers.log
#SBATCH --ntasks=1
#SBATCH --mem=50000
#SBATCH --time=12:00:00
#SBATCH --job-name=startJobs
srun --time=12:00:00 --mem=50000 ~/pythonProjects/env/bin/python2.7 -W ignore HyperoptStartWorkers.py
