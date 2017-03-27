#!/bin/bash
#SBATCH --cpus-per-task=1
#SBATCH --time=00:30:00
#SBATCH --mem=10110
#SBATCH --output=slurmOut.log
source ~/pythonProjects/tf_rnn/preInit.sh && ?job?
