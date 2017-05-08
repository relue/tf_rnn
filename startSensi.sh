#!/bin/bash
#SBATCH --output=logs/startSensi.log
#SBATCH --time=03:00:00
#SBATCH --mem-per-cpu=2500
#SBATCH --job-name=startSensi
#SBATCH --ntasks=1
#SBATCH --cpus-per-task=1
srun ~/pythonProjects/env/bin/python2.7 -W ignore parallelExecutor.py
