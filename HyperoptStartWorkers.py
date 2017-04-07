import itertools
import collections
import json
import subprocess
import logging
import os
import time
import random

def createBatchFile(singleCommand):
    with open("hyperOptScript.sh", "rt") as fin:
        with open("hyperOptScriptExecute.sh", "wt") as fout:
            for line in fin:
                line = line.replace('?job?', singleCommand)
                fout.write(line)
import experimentConfig


import socket
s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
s.connect(("8.8.8.8", 80))
ip=s.getsockname()[0]
s.close()

workerCount = 20000
log = open("logs/hyperoptStartWorker.log", "w")
logDB = open("logs/mongo.log", "w")
createBatchFile("srun --time=02:00:00 --mem=10000 sh ~/pythonProjects/tf_rnn/HyperoptWorkerWrapper.sh "+ip)
startDB = "mongod --dbpath ~/mongo/mongodb/mongodb-linux-x86_64-3.4.2/data/db"
startOptimizer = "source ../env/bin/activate; python HyperoptOptimizer.py "+ip

p = subprocess.Popen(startDB, stdout=logDB, stderr=logDB, shell=True)
p = subprocess.Popen(startOptimizer, stdout=log, stderr=log, shell=True)
for i in range(1, workerCount):
    p = subprocess.Popen("sbatch hyperOptScriptExecute.sh", stdout=log, stderr=log, shell=True)
    time.sleep(0.3)

while 1:
    hold=1