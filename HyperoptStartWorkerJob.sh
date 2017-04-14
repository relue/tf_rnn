#!/bin/bash
#SBATCH --output=logs/SlurmHyperoptStartWorkers.log
#SBATCH --mem=50000
#SBATCH --time=24:00:00
#SBATCH --job-name=startJobs
#SBATCH --ntasks=1
#SBATCH --mem-per-cpu=2000M
srun --time=24:00:00 --ntasks=1 --cpus-per-task=2  ~/pythonProjects/env/bin/python2.7 -W ignore HyperoptStartWorkers.py
