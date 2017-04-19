#!/bin/bash
#SBATCH --output=logs/SlurmHyperoptStartWorkers.log
#SBATCH --time=12:00:00
#SBATCH --mem-per-cpu=20000
#SBATCH --job-name=startJobs
#SBATCH --ntasks=1
#SBATCH --cpus-per-task=8
srun ~/pythonProjects/env/bin/python2.7 -W ignore HyperoptStartWorkers.py
