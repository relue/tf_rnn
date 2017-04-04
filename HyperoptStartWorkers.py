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

for filename in os.listdir("batchScripts/"):
    os.remove("batchScripts/"+filename)

ip = '172.24.32.17'
workerCount = 10000
log = open("hyperoptStartWorker.log", "w")

createBatchFile("srun --cpus-per-task=1 --time=01:00:00 --mem=3110 ~/pythonProjects/env/bin/python2.7 -W ignore ~/pythonProjects/tf_rnn/HyperoptWorkerWrapper.py")

for i in range(1, workerCount):

    p = subprocess.Popen("sbatch batchScripts/hyperOptScript.sh", stdout=log, stderr=log, shell=True)

while 1:
    time.sleep(10)
    p= subprocess.Popen("cat hyperoptStartWorker.log", stdout=subprocess.PIPE, stderr=None, shell=True)
    result = p.communicate()[0]
    print result
