#!/bin/bash
#SBATCH --output=logs/SlurmHyperoptStartWorkers.log
#SBATCH --time=08:00:00
#SBATCH --mem=25000
#SBATCH --job-name=startJobs
#SBATCH --ntasks=1
#SBATCH --cpus-per-task=6
srun ~/pythonProjects/env/bin/python2.7 -W ignore HyperoptStartWorkers.py
