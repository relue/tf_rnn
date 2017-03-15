import itertools
import modelKeras
import collections
import json
import subprocess

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

pre = subprocess.Popen("~/pythonProjects/tf_rnn/preInit.sh ", shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)

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

    p = subprocess.Popen("srun --gres=cpu:16 --time=00:30:00 --mem=40110  --pty ~/pythonProjects/env/bin/python2.7 ~/pythonProjects/tf_rnn/singleExecution.py "+data_str, shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
    for line in iter(p.stdout.readline, ''): print line,
    retval = p.wait()

    if permIndex == maxIters:
        break
    permIndex += 1
