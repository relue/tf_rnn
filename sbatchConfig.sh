#!/bin/bash
#SBATCH --output=logs/sensiJob.log
#SBATCH --mem-per-cpu=5100
#SBATCH --time=06:00:00
source ~/pythonProjects/tf_rnn/preInit.sh && ?job?
