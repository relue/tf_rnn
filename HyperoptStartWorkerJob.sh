#!/bin/bash
#SBATCH --output=logs/SlurmHyperoptStartWorkers.log
#SBATCH --time=01:00:00
#SBATCH --mem=50000
#SBATCH --job-name=startJobs
#SBATCH --ntasks=1
#SBATCH --cpus-per-task=16
srun ~/pythonProjects/env/bin/python2.7 -W ignore HyperoptStartWorkers.py
