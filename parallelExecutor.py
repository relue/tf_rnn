import itertools
import collections
import json
import subprocess
import logging
logging.basicConfig(filename='parallelExec.log',level=logging.DEBUG)

# Define Parameter Settings
maxIters = 20
parameters = collections.OrderedDict((
("learningRate", [0.001, 0.01, 0.05, 0.1, 0.2, 0.4, 0.7]),
("hiddenLayer"  , [1, 2, 3, 4]),
("hiddenNodes" , [2, 4, 8, 16, 32, 62, 128]),
("optimizers" , ['adam', 'sgd']),
("timeWindow" , [1, 12, 24, 48, 96]),
("batchSize" , [1,10,20,30]),
("epochSize" , [1, 10, 50]),
("activationFunction" , ["tanh", "sigmoid"])
))
permMatrix = list(itertools.product(*parameters.values()))
iters = len(permMatrix)
print "Anzahl der Permutationen:"+str(iters)
print (permMatrix)
log = open("parallelExecDetail.log", "a")

permIndex = 0
for el in permMatrix:
    keys=parameters.keys()
    setting = {
        "learningRate" : el[keys.index("learningRate")],
        "hiddenNodes" : el[keys.index("hiddenNodes")],
        "timeWindow" : el[keys.index("timeWindow")],
        "optimizers" : el[keys.index("optimizers")],
        "batchSize" : el[keys.index("batchSize")],
        "epochSize" : el[keys.index("epochSize")],
        "indexID" : permIndex
    }
    data_str=json.dumps(setting)

#env/bin/python2.7 tensorflow/tensorflow/examples/tutorials/mnist/fully_connected_feed.py
    command = "srun --gres=cpu:16 --time=00:05:00 --mem=10110  --pty " \
              "~/pythonProjects/env/bin/python2.7 ~/pythonProjects/tf_rnn/singleExecution.py '"+data_str + "'"
    p = subprocess.Popen(command, shell=True, stdout=log)
    logging.warning('command'+str(permIndex)+": "+command)

    if permIndex == maxIters:
        break
    permIndex += 1
