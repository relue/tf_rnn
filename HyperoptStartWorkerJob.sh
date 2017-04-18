#!/bin/bash
#SBATCH --output=logs/SlurmHyperoptStartWorkers.log
#SBATCH --time=24:00:00
#SBATCH --mem-per-cpu=20000
#SBATCH --job-name=startJobs
#SBATCH --ntasks=1

srun --mem-per-cpu=20000 --time=24:00:00 --ntasks=1  ~/pythonProjects/env/bin/python2.7 -W ignore HyperoptStartWorkers.py
