#!/bin/bash
module load gcc/4.9.1
module load cuda/8.0.44

export LD_LIBRARY_PATH="$LD_LIBRARY_PATH:/sw/taurus/libraries/cuda/8.0.44/lib64:/sw/taurus/libraries/cuda/8.0.44/extras/CUPTI/lib64:${HOME}/libraries/cudnn/lib64:"
export CUDA_HOME="/sw/taurus/libraries/cuda/8.0.44"
