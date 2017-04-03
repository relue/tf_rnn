import hyperopt
from hyperopt import fmin,tpe, hp
from hyperopt.mongoexp import MongoTrials
import modelKeras
import HyperoptObjective



'''
continousParameterBounds = {
        "learningRate": (0,0.1),
        "DropoutProp": (0.0,0.3),
        "l1Penalty": (0.0001,0.01)
    }

    discreteParameterRanges = {
        "activationFunction": ["tanh", "sigmoid", "relu"],
        "hiddenNodes": range(10,300),
        "optimizer": ['adam', 'sgd', 'rms','ada', 'adadelta'],
        "timeWindow": range(10,199),
        "batchSize": range(1,101),
        "hiddenLayers": range(1,5),
        "weightInit": ["zero", "one", "normal", "glorot_uniform", "lecun_uniform", "glorot_normal"],
        "earlyStopping": [True, False],
        "useHoliday": [True, False],
        "useWeekday": [True, False],
        "noFillZero": [True, False],
        "stationIDs": range(1,13),
    }
'''

#{\"optimizer\": \"adam\", \"hiddenNodes\": 2, \"timeWindow\": 1, \"batchSize\": 1, \"indexID\": 2, \"learningRate\": 0.001, \"epochSize\": 10}
import sys

def objective(x):
    print x
    import imp
    modelKeras = imp.load_source('modelKeras', '/home/dev/PycharmProjects/untitled/tf_rnn/modelKeras.py')
    modelOut = modelKeras.KerasModel(**x)
    data = {}
    data['loss'] = modelOut.results['loss'][-1]
    data['val_loss'] = modelOut.results['val_loss'][-1]
    data['test_loss'] = modelOut.results['test_loss'][-1]

    return 2

def minMe (x):
    import math
    return math.sin(x)

space =  {
        'activationFunction1': hp.choice('activationFunction1', ["tanh", "sigmoid", "relu"]),
        'learningRate': hp.uniform('learningRate', 0, 0.4),

    }

#print hyperopt.pyll.stochastic.sample(space)
trials = MongoTrials('mongo://localhost:27017/foo_db/jobs', exp_key='rnn4')
best = fmin(fn=objective, space=space, trials=trials, algo=hyperopt.rand.suggest, max_evals=10, verbose=1)
print best
