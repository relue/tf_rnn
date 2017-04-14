#!/bin/bash
#SBATCH --output=logs/SlurmHyperoptStartWorkers.log
#SBATCH --time=24:00:00
#SBATCH --mem=40000
#SBATCH --job-name=startJobs
#SBATCH --ntasks=1

srun --mem=40000 --time=24:00:00 --ntasks=1 --cpus-per-task=1  ~/pythonProjects/env/bin/python2.7 -W ignore HyperoptStartWorkers.py
