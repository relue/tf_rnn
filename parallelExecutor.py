import itertools
import collections
import json
import subprocess
import logging
import os
import time

def createBatchFile(singleCommand, id):
     with open("sbatchConfig.sh", "rt") as fin:
        with open("batchScripts/script"+str(id)+".sh", "wt") as fout:
            for line in fin:
                fout.write(line.replace('?job?', singleCommand))

#createBatchFile("srun --cpus-per-task=1 --time=00:30:00 --mem=3110 ~/pythonProjects/env/bin/python2.7 -W ignore ~/pythonProjects/tf_rnn/singleExecution.py", 2)

maxIters = 200000
parameters = collections.OrderedDict((
("learningRate", [0.001, 0.01, 0.05, 0.1, 0.2, 0.4, 0.7]),
#("hiddenLayer"  , [1, 2, 3, 4]),
("hiddenNodes" , [2, 4, 8, 16, 32, 62, 128,256]),
("stationID" , [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11]),
("optimizers" , ['adam', 'sgd']),
("timeWindow" , [1, 12, 24, 36, 48, 96]),
("batchSize" , [1,10,20,30]),
("epochSize" , [100]),
#("activationFunction" , ["tanh", "sigmoid"])
))
permMatrix = list(itertools.product(*parameters.values()))
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
    setting = {
        "learningRate" : el[keys.index("learningRate")],
        "hiddenNodes" : el[keys.index("hiddenNodes")],
        "timeWindow" : el[keys.index("timeWindow")],
        "optimizer" : el[keys.index("optimizers")],
        "batchSize" : el[keys.index("batchSize")],
        "epochSize" : el[keys.index("epochSize")],
        "stationID" : el[keys.index("stationID")],
        "indexID" : permIndex
    }
    data_str=json.dumps(setting)
    createBatchFile("srun --cpus-per-task=1 --time=01:00:00 --mem=3110 ~/pythonProjects/env/bin/python2.7 -W ignore ~/pythonProjects/tf_rnn/singleExecution.py '"+data_str + "' ", permIndex)
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
