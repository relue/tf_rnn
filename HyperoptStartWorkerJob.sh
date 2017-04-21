#!/bin/bash
#SBATCH --output=logs/SlurmHyperoptStartWorkers.log
#SBATCH --time=12:00:00
#SBATCH --mem=10000
#SBATCH --job-name=startJobs
#SBATCH --ntasks=1
#SBATCH --cpus-per-task=4
srun ~/pythonProjects/env/bin/python2.7 -W ignore HyperoptStartWorkers.py
