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
               # line = line.replace('?jobname?', str(id))
                fout.write(line)
import experimentConfig


log = open("logs/parallelSensi.log", "w")
for filename in os.listdir("jobResults/"):
    os.remove("jobResults/"+filename)
for filename in os.listdir("batchScripts/"):
    os.remove("batchScripts/"+filename)

def executeConfig(setting, permIndex):
    setting["indexID"] = permIndex
    data_str = json.dumps(setting)
    createBatchFile(
            "srun ~/pythonProjects/env/bin/python2.7 -W ignore ~/pythonProjects/tf_rnn/singleExecution.py '" + data_str + "' 0",
        data_str,permIndex)
    p = subprocess.Popen("sbatch batchScripts/script" + str(permIndex) + ".sh", stdout=log, stderr=log, shell=True)

maxResolution = 100
c = experimentConfig.Config()
#optHyperparams = c.sensiExperiment1

optHyperparams = c.getBestAsDict("tpe_3", hypeOnly=True)

runs = []
runs.append(optHyperparams)
for param in c.sensiIntervalsOptimizer:
    values = c.sensiIntervalsOptimizer[param]
    if c.parameterTypeDiscrete[param] == True:
        ''' if c.parameterNumeric[param]:
            steps = len(values)
            toCheck = range(1,len(values))
        '''
        for pValue in values:
            newRow = optHyperparams.copy()
            newRow[param] = pValue
            print 'change '+param+' to '+str(pValue)+ 'Rest'
            print newRow
            runs.append(newRow)
    else:
        upV = values[1]
        downV = values[0]
        stepSize = float(upV) / float(maxResolution)
        newRow = optHyperparams.copy()
        newRow[param] = downV
        runs.append(newRow)
        for i in range (1,maxResolution):
            newRow = optHyperparams.copy()
            pValue = stepSize*i
            newRow[param] = pValue
            print 'change ' + param + ' to ' + str(pValue) + 'Rest'
            runs.append(newRow)

print str(len(runs)) + " runs planned"

permIndex = 1
p = subprocess.Popen("ulimit -u 10000", stdout=log, stderr=log, shell=True)

for run in runs:
    run["indexID"] = permIndex
    executeConfig(run,permIndex)
    time.sleep(0.2)
    permIndex += 1
