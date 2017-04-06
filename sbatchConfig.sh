#!/bin/bash
#SBATCH --output=slurmOut.log
#SBATCH --ntasks=1
#SBATCH --mem=10000
source ~/pythonProjects/tf_rnn/preInit.sh && ?job?
