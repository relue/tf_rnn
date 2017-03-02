#!/bin/bash
#module load gcc/4.9.1
module load cuda/8.0.44

export LD_LIBRARY_PATH="$LD_LIBRARY_PATH:/sw/taurus/libraries/cuda/8.0.44/lib64:/sw/taurus/libraries/cuda/8.0.44/extras/CUPTI/lib64:${HOME}/libraries/cudnn/lib64:"
export CUDA_HOME="/sw/taurus/libraries/cuda/8.0.44"
#env/bin/python2.7 tensorflow/tensorflow/examples/tutorials/mnist/fully_connected_feed.py 
srun --gres=gpu:4 --time=00:30:00 --mem=40110  --pty ~/pythonProjects/env/bin/python2.7 $1

#srun --cpus-per-task=16 --time=00:30:00 --mem=40110  --pty ~/pythonProjects/env/bin/python2.7 $1



