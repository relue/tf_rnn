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


log = open("parallelExecDetail.log", "w")
for filename in os.listdir("jobResults/"):
    os.remove("jobResults/"+filename)
for filename in os.listdir("batchScripts/"):
    os.remove("batchScripts/"+filename)

def executeConfig(setting, permIndex):
    setting["indexID"] = permIndex
    data_str = json.dumps(setting)
    createBatchFile(
            "srun --time=02:00:00 --mem-per-cpu=2510 ~/pythonProjects/env/bin/python2.7 -W ignore ~/pythonProjects/tf_rnn/singleExecution.py '" + data_str + "' 0",
        data_str,permIndex)
    p = subprocess.Popen("sbatch batchScripts/script" + str(permIndex) + ".sh", stdout=log, stderr=log, shell=True)

maxResolution = 50
data = {}
data["earlyStopping"] = True
data["standardizationType"] = "zscore"
data["stationIDs"] = [13]
data["noFillZero"] = True
data["useHoliday"] = True
data["useWeekday"] = True
data["earlyStopping"] = True

data["epochSize"] = 15
data["batchSize"] = 1
data["learningRate"] = 0.001
data["activationFunction"] = "tanh"
data["l1Penalty"] = 0.000001
data["DropoutProp"] = 0.001
data["hiddenNodes"] = 30
data["hiddenLayers"] = 20
data["optimizer"] = "adam"
data["weightInit"] = "lecun_uniform"
data["timeWindow"] = 7*24

c = experimentConfig.Config()
runs = []
for param in c.experimentConfigWide:
    values = c.experimentConfigWide[param]
    if c.parameterTypeDiscrete[param] == True:
        ''' if c.parameterNumeric[param]:
            steps = len(values)
            toCheck = range(1,len(values))
        '''
        for pValue in values:
            newRow = data.copy()
            newRow[param] = pValue
            runs.append(newRow)
    else:
        upV = values[1]
        downV = values[0]
        stepSize = float(upV) / float(maxResolution)
        newRow = data.copy()
        newRow[param] = downV
        runs.append(newRow)
        for i in range (1,maxResolution+1):
            newRow = data.copy()
            newRow[param] = stepSize*i
            runs.append(newRow)
print runs
print runs




c.experimentConfigWide
c.parameterTypeDiscrete
analyze = []

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
