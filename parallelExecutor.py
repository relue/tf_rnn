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
        with open("batchScripts/script"+str(id)+".sh", "wt") as fout:
            for line in fin:
                fout.write(line.replace('?job?', singleCommand))
import experimentConfig
#createBatchFile("srun --cpus-per-task=1 --time=00:30:00 --mem=3110 ~/pythonProjects/env/bin/python2.7 -W ignore ~/pythonProjects/tf_rnn/singleExecution.py", 2)

maxIters =5000
parameters = experimentConfig.Config.parametersAddtionalInput
permMatrix = list(itertools.product(*parameters.values()))
#permMatrix = experimentConfig.Config.generateRandom()
random.shuffle(permMatrix)
iters = len(permMatrix)
print "Anzahl der Permutationen:"+str(iters)
log = open("parallelExecDetail.log", "w")
permIndex = 0
p = subprocess.Popen("scancel -u s2071275",  stdout=log, stderr=log, shell=True)
for filename in os.listdir("jobResults/"):
    os.remove("jobResults/"+filename)
for filename in os.listdir("batchScripts/"):
    os.remove("batchScripts/"+filename)
preCommand = "export PYTHONWARNINGS='ignore' && source ~/pythonProjects/tf_rnn/preInit.sh && "
command = ""

for el in permMatrix:
    keys=parameters.keys()
    setting = {}
    for key in keys:
        setting[key] = el[keys.index(key)]
    setting["indexID"] = permIndex
    data_str=json.dumps(setting)
    createBatchFile("srun --cpus-per-task=1 --time=01:00:00 --mem=3110 ~/pythonProjects/env/bin/python2.7 -W ignore ~/pythonProjects/tf_rnn/singleExecution.py '"+data_str + "' 0", permIndex)
    p = subprocess.Popen("sbatch batchScripts/script"+str(permIndex)+".sh",  stdout=log, stderr=log, shell=True)
    #time.sleep(1)
    permIndex += 1
    if permIndex >= maxIters:
        break

    print 'permIndex:'+str(permIndex)

while 1:
    time.sleep(10)
    p= subprocess.Popen("cat parallelExecDetail.log", stdout=subprocess.PIPE, stderr=None, shell=True)
    result = p.communicate()[0]
    print result
