import hyperopt
from hyperopt import fmin,tpe, hp
from hyperopt.mongoexp import MongoTrials
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
import os.path
import os
dir_path = os.path.dirname(os.path.realpath(__file__))


def objective(x):
    path = x["dirPath"]
    del x["dirPath"]
    from hyperopt import  STATUS_OK
    import imp

    modelKeras = imp.load_source('modelKeras', path+'/modelKeras.py')
    modelOut = modelKeras.KerasModel(**x)
    data = {}
    data['loss'] = modelOut.results['loss'][-1]
    data['val_loss'] = modelOut.results['val_loss'][-1]
    data['test_loss'] = modelOut.results['test_loss'][-1]
    data['status'] = STATUS_OK
    data = dict(x.items() + data.items())
    return data

space =  {
        'earlyStopping': True,
        'epochSize' : 1,
        "learningRate": hp.uniform('learningRate', 0 , 0.4),
        "DropoutProp": hp.uniform('DropoutProp', 0.4, 0.8),
        "l1Penalty": hp.uniform('l1Penalty',0.0001, 0.01),
        "activationFunction": hp.choice('activationFunction',["tanh", "sigmoid", "relu"]),
        "hiddenNodes": hp.choice('hiddenNodes', range(10,300)),
        "optimizer": hp.choice('optimizer', ['adam', 'sgd', 'rms','ada', 'adadelta']),
        "timeWindow": hp.choice('timeWindow', range(10,199)),
        "batchSize": hp.choice('batchSize', range(1,101)),
        "hiddenLayers": hp.choice('hiddenLayers', range(1,5)),
        "weightInit": hp.choice('weightInit', ["zero", "one", "normal", "glorot_uniform", "lecun_uniform", "glorot_normal"]),
        "earlyStopping": hp.choice('earlyStopping', [True, False]),
        "useHoliday": hp.choice('useHoliday', [True, False]),
        "useWeekday": hp.choice('useWeekday', [True, False]),
        "noFillZero": hp.choice('noFillZero', [True, False]),
        "stationIDs": [hp.choice('stationIDs', range(1,13))],
        "dirPath": dir_path
    }
ip = sys.argv[1]
#print hyperopt.pyll.stochastic.sample(space)
trials = MongoTrials('mongo://'+ip+':27017/foo_db/jobs', exp_key='finalFun')
best = fmin(fn=objective, space=space, trials=trials, algo=hyperopt.rand.suggest, max_evals=200000, verbose=2)
print best
