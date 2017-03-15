#!/bin/bash
sh preInit.sh
#env/bin/python2.7 tensorflow/tensorflow/examples/tutorials/mnist/fully_connected_feed.py 
srun  --gres=gpu:1 --time=00:30:00 --mem=40110  --pty ~/pythonProjects/env/bin/python2.7 $1

#srun --cpus-per-task=16 --time=00:30:00 --mem=30110  --pty ~/pythonProjects/env/bin/python2.7 $1



