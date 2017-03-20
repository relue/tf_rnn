import itertools
import collections
import json
import subprocess
import logging
import os
import time

maxIters = 500
parameters = collections.OrderedDict((
("learningRate", [0.001, 0.01, 0.05, 0.1, 0.2, 0.4, 0.7]),
#("hiddenLayer"  , [1, 2, 3, 4]),
("hiddenNodes" , [2, 4, 8, 16, 32, 62, 128]),
("optimizers" , ['adam', 'sgd']),
("timeWindow" , [1, 12, 24, 48, 96]),
("batchSize" , [1,10,20,30]),
("epochSize" , [1, 10, 50]),
#("activationFunction" , ["tanh", "sigmoid"])
))
permMatrix = list(itertools.product(*parameters.values()))
iters = len(permMatrix)
print "Anzahl der Permutationen:"+str(iters)
log = open("parallelExecDetail.log", "w")
permIndex = 0

for filename in os.listdir("jobResults/"):
    os.remove("jobResults/"+filename)
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
        "indexID" : permIndex
    }
    data_str=json.dumps(setting)
    print data_str
#env/bin/python2.7 tensorflow/tensorflow/examples/tutorials/mnist/fully_connected_feed.py
    command = preCommand+"srun --cpus-per-task=1 --time=00:30:00 --mem=3110 ~/pythonProjects/env/bin/python2.7 -W ignore ~/pythonProjects/tf_rnn/singleExecution.py '"+data_str + "' "
    p = subprocess.Popen(command,  stdout=log, stderr=log, shell=True)
    time.sleep(3)
    if permIndex >= maxIters:
        break
    permIndex += 1
    print 'permIndex:'+str(permIndex)


time.sleep(3)
p= subprocess.Popen("cat parallelExecDetail.log", stdout=subprocess.PIPE, stderr=None, shell=True)
result = p.communicate()[0]
print result
