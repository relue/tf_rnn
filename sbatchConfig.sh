#!/bin/bash
#SBATCH --output=logs/sensiJob.log
#SBATCH --mem-per-cpu=2500
#SBATCH --time=05:00:00
source ~/pythonProjects/tf_rnn/preInit.sh && ?job?
