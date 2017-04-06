#!/bin/bash
#SBATCH --output=logs/SlurmHyperoptStartWorkers.log
#SBATCH --ntasks=1
#SBATCH --mem=10000
#SBATCH --time=24:00:00
srun --time=24:00:00 ~/pythonProjects/env/bin/python2.7 -W ignore HyperoptStartWorkers.py
