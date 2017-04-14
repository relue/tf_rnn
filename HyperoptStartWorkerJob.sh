#!/bin/bash
#SBATCH --output=logs/SlurmHyperoptStartWorkers.log
#SBATCH --mem=50000
#SBATCH --time=24:00:00
#SBATCH --job-name=startJobs
srun --time=24:00:00 --cpus-per-task=3 --mem=50000 ~/pythonProjects/env/bin/python2.7 -W ignore HyperoptStartWorkers.py
