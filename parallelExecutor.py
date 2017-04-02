import itertools
import collections
import json
import subprocess
import logging
import os
import time
import random
def createBatchFile(singleCommand,parameters, id):
     with open("sbatchConfig.sh", "rt") as fin:
        with open("batchScripts/script"+str(id)+".sh", "wt") as fout:
            for line in fin:
                line = line.replace('?job?', singleCommand)
                line = line.replace('?jobname?', parameters)
                fout.write(line)
import experimentConfig

isRandomSearch = True
if isRandomSearch:
    c = experimentConfig.Config()
    randVecDef = [
            "learningRate",
            "DropoutProp",
            "l1Penalty",
            "activationFunction",
            "hiddenNodes",
            "optimizer",
            "timeWindow",
            "batchSize",
            "hiddenLayers",
            "weightInit",
            "earlyStopping",
            "noFillZero",
    ]
    maxRandomTrials = 1

maxIters = 10
parameters = experimentConfig.Config.parametersAddtionalInput
permMatrix = list(itertools.product(*parameters.values()))

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

def executeConfig(setting, permIndex):
    setting["indexID"] = permIndex
    data_str = json.dumps(setting)
    createBatchFile(
            "srun --cpus-per-task=1 --time=01:00:00 --mem=3110 ~/pythonProjects/env/bin/python2.7 -W ignore ~/pythonProjects/tf_rnn/singleExecution.py '" + data_str + "' 0",
        data_str,permIndex)
    p = subprocess.Popen("sbatch batchScripts/script" + str(permIndex) + ".sh", stdout=log, stderr=log, shell=True)
if isRandomSearch:
    for permIndex in range(1,maxRandomTrials):
        setting = c.generateRandomVektor(randVecDef)
        executeConfig(setting, permIndex)

else:
    for el in permMatrix:
        keys=parameters.keys()
        setting = {}
        for key in keys:
            setting[key] = el[keys.index(key)]
        executeConfig(setting,permIndex)

        permIndex += 1
        if permIndex >= maxIters:
            break



while 1:
    time.sleep(10)
    p= subprocess.Popen("cat parallelExecDetail.log", stdout=subprocess.PIPE, stderr=None, shell=True)
    result = p.communicate()[0]
    print result
