import hyperopt
from hyperopt import fmin,tpe, hp
from hyperopt.mongoexp import MongoTrials
import HyperoptObjective
import logging
logging.basicConfig(filename='logs/fminLog.log', level=10)



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
    import math

    modelKeras = imp.load_source('modelKeras', path+'/modelKeras.py')
    modelOut = modelKeras.KerasModel(**x)
    data = {}
    data = modelOut.results
    data['status'] = STATUS_OK
    data['loss'] = data['val_rmse']
    if math.isnan(data['loss']) == True:
        data['loss'] = 9999999
    data = dict(x.items() + data.items())
    return data



space_1 =  {
        'standardizationType': hp.choice('standardizationType', ["minmax", "zscore"]),
        'epochSize' : hp.choice('epochSize', range(5,30)),
        "learningRate": hp.uniform('learningRate', 0 , 1),
        "DropoutProp": hp.uniform('DropoutProp', 0.0001, 0.99),
        "l1Penalty": hp.uniform('l1Penalty',0.0001, 0.99),
        "activationFunction": hp.choice('activationFunction',["tanh", "sigmoid", "relu"]),
        "hiddenNodes": hp.choice('hiddenNodes', range(10,300)),
        "optimizer": hp.choice('optimizer', ['adam', 'sgd', 'rms','ada', 'adadelta']),
        "timeWindow": hp.choice('timeWindow', range(1,336)),
        "batchSize": hp.choice('batchSize', range(1,101)),
        "hiddenLayers": hp.choice('hiddenLayers', range(1,10)),
        "weightInit": hp.choice('weightInit', ["zero", "one", "normal", "glorot_uniform", "lecun_uniform", "glorot_normal"]),
        "useHoliday": hp.choice('useHoliday', [True, False]),
        "useWeekday": hp.choice('useWeekday', [True, False]),
        "dirPath": dir_path
    }

space =  {
        'standardizationType': hp.choice('standardizationType', ["zscore"]),
        'epochSize' : hp.choice('epochSize', range(5,30)),
        "learningRate": hp.uniform('learningRate', 0 , 1),
        "DropoutProp": hp.uniform('DropoutProp', 0.0001, 0.99),
        "l1Penalty": hp.uniform('l1Penalty',0.0001, 0.99),
        "activationFunction": hp.choice('activationFunction',["tanh", "sigmoid", "relu"]),
        "hiddenNodes": hp.choice('hiddenNodes', range(10,300)),
        "optimizer": hp.choice('optimizer', ['adam', 'sgd', 'rms','ada', 'adadelta']),
        "timeWindow": hp.choice('timeWindow', range(24,337, 24)),
        "batchSize": hp.choice('batchSize', range(1,101)),
        "hiddenLayers": hp.choice('hiddenLayers', range(1,4)),
        "weightInit": hp.choice('weightInit', ["glorot_normal"]),
        "useHoliday": hp.choice('useHoliday', [True]),
        "useWeekday": hp.choice('useWeekday', [True]),
        "dirPath": dir_path
    }
ip = sys.argv[1]
#print hyperopt.pyll.stochastic.sample(space)
#finalCountdown random
#finalCountdown_TPE tpe
#db_experiment1 = "final_db"
#db_experiment2 = "db_tpe2"
db_experiment2 = "db_tpe3"
key_experiment1 = "rand1"
key_experiment2 = "firstTpe"
key = key_experiment2
db = db_experiment2

trials = MongoTrials('mongo://127.0.0.1:27017/'+db+'/jobs', exp_key=key)
best = fmin(fn=objective, space=space, trials=trials, algo=hyperopt.tpe.suggest, max_evals=300000, verbose=1)
print best
