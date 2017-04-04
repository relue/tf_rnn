import itertools
import collections
import json
import subprocess
import logging
import os
import time
import random
def createBatchFile(singleCommand, id):
     with open("sbatchConfig.sh", "rt") as fin:
        with open("batchScripts/hyperOptScript"+str(id)+".sh", "wt") as fout:
            for line in fin:
                line = line.replace('?job?', singleCommand)
               # line = line.replace('?jobname?', str(id))
                fout.write(line)
import experimentConfig

for filename in os.listdir("batchScripts/"):
    os.remove("batchScripts/"+filename)

ip = '172.24.32.17:27017'
workerCount = 1000
log = open("hyperoptWorker.log", "w")
workerCommand= 'hyperopt-mongo-worker --mongo='+ip+':27017/foo_db --poll-interval=0.1'
for i in range(1, workerCount):
    createBatchFile(workerCommand, id)
    createBatchFile(
            "srun --cpus-per-task=1 --time=01:00:00 --mem=3110 "+workerCommand,i)
    p = subprocess.Popen("sbatch batchScripts/hyperOptScript" + str(i) + ".sh", stdout=log, stderr=log, shell=True)

while 1:
    time.sleep(10)
    p= subprocess.Popen("cat hyperoptWorker.log", stdout=subprocess.PIPE, stderr=None, shell=True)
    result = p.communicate()[0]
    print result
