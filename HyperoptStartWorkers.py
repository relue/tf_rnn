import itertools
import collections
import json
import subprocess
import logging
import os
import time
import random
def createBatchFile(singleCommand):
     with open("sbatchConfig.sh", "rt") as fin:
        with open("batchScripts/hyperOptScript.sh", "wt") as fout:
            for line in fin:
                line = line.replace('?job?', singleCommand)
               # line = line.replace('?jobname?', str(id))
                fout.write(line)
import experimentConfig


import socket
s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
s.connect(("8.8.8.8", 80))
ip=s.getsockname()[0]
s.close()

workerCount = 10
log = open("logs/hyperoptStartWorker.log", "w")
logDB = open("logs/mongo.log", "w")
createBatchFile("srun ~/pythonProjects/env/bin/python2.7 -W ignore ~/pythonProjects/tf_rnn/HyperoptWorkerWrapper.py "+ip)
p = subprocess.Popen("startm", stdout=logDB, stderr=logDB, shell=True)
for i in range(1, workerCount):
    p = subprocess.Popen("sbatch batchScripts/hyperOptScript.sh", stdout=log, stderr=log, shell=True)

p = subprocess.Popen("source ../env/bin/activate; python HyperoptOptimizer.py ", stdout=log, stderr=log, shell=True)
