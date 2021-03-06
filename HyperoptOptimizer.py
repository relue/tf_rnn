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
    import numpy as np
    np.random.seed(1337)
    convInt = ["batchSize", "timeWindow", "hiddenNodes","epochSize", "hiddenLayers"]
    for param in convInt:
        x[param] = int(x[param])
    modelKeras = imp.load_source('modelKeras', path+'/modelKeras.py')
    modelOut = modelKeras.KerasModel(**x)
    data = {}
    data = modelOut.results
    data['status'] = STATUS_OK
    data['loss'] = data['val_rmse']
    if math.isnan(data['loss']) == True:
        data['loss'] = 80000
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

#fast ganzer Bereich
db_experiment3 = "db_tpe3"
spaceWideFiltered =  {
        'standardizationType': hp.choice('standardizationType', ["zscore"]), #da in Voruntersuchung besser
        'epochSize' : hp.choice('epochSize', range(5,30)),
        "learningRate": hp.uniform('learningRate', 0 , 1), # niedrig empfohlen
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

db_experiment3 = "db_tpe4"

#fast ganzer Bereich tpe2b
spaceNarrow=  {
        'epochSize' : hp.quniform('epochSize', 8, 40, 1),#evtl. erhoehen
        "learningRate": hp.loguniform('learningRate', -7.6 , -1.2), # (0.0005,0.3)
        "DropoutProp": hp.loguniform('DropoutProp', -6.9, -0.51), # (0.001,0.6)
        "l1Penalty": hp.loguniform('l1Penalty', -11.51, -4.6), # (0,00001,0.01) # noch weiter verkleinern
        "activationFunction": hp.choice('activationFunction',["tanh", "relu"]),
        "hiddenNodes": hp.quniform('hiddenNodes', 10,200, 10),# evtl nochmal erhoehen, feiner?
        "optimizer": hp.choice('optimizer', ['adam', 'sgd', 'rms']),
        "timeWindow": hp.quniform('timeWindow', 24, 337, 24), # eventuell feiner
        "batchSize": hp.quniform('batchSize', 1, 100, 1),
        "hiddenLayers": hp.quniform('hiddenLayers', 1,4,1),
        "weightInit": hp.choice('weightInit', ["glorot_normal","lecun_uniform"]),
        "dirPath": dir_path
    }

#fast ganzer Bereich tpe_3
spaceNarrowTuned=  {
        'epochSize' : hp.quniform('epochSize', 8, 40, 1),#evtl. erhoehen
        "learningRate": hp.loguniform('learningRate', -7.6 , -1.2), # (0.0005,0.3)
        "DropoutProp": hp.loguniform('DropoutProp', -6.9, -0.51), # (0.001,0.6)
        "l1Penalty": hp.loguniform('l1Penalty', -13.81, -4.6), # (0,000001,0.01) # noch weiter verkleinern
        "activationFunction": hp.choice('activationFunction',["tanh", "relu"]),
        "hiddenNodes": hp.quniform('hiddenNodes', 10,200, 5),# evtl nochmal erhoehen, feiner?
        "optimizer": hp.choice('optimizer', ['adam', 'sgd', 'rms']),
        "timeWindow": hp.quniform('timeWindow', 24, 337, 1), # eventuell feiner
        "batchSize": hp.quniform('batchSize', 1, 100, 1),
        "hiddenLayers": hp.quniform('hiddenLayers', 1,4,1),
        "weightInit": hp.choice('weightInit', ["glorot_normal","lecun_uniform"]),
        "dirPath": dir_path
    }

#fast ganzer Bereich tpe_4
spaceCompleteNarrow=  {
        'epochSize' : hp.quniform('epochSize', 8, 40, 1),#evtl. erhoehen
        "learningRate": hp.loguniform('learningRate', -11.51 , -1.2), # (0.00001,0.3)
        "DropoutProp": hp.loguniform('DropoutProp', -6.9, -0.51), # (0.001,0.6)
        "l1Penalty": hp.loguniform('l1Penalty', -18.42, -4.6), # (10^-8,0.01) # noch weiter verkleinern
        "activationFunction": hp.choice('activationFunction',["tanh", "sigmoid","relu"]),
        "hiddenNodes": hp.quniform('hiddenNodes', 10,300, 5),# evtl nochmal erhoehen, feiner?
        "optimizer": hp.choice('optimizer', ['adam', 'sgd', 'rms']),
        "timeWindow": hp.quniform('timeWindow', 24, 337, 1), # eventuell feiner
        "batchSize": hp.quniform('batchSize', 1, 100, 1),
        "hiddenLayers": hp.quniform('hiddenLayers', 1,4,1),
        "weightInit": hp.choice('weightInit', ["zero", "one", "normal", "glorot_uniform", "lecun_uniform", "glorot_normal"]),
        "useHoliday": hp.choice('useHoliday', [True, False]),
        "useWeekday": hp.choice('useWeekday', [True, False]),
        "standardizationType": hp.choice('standardizationType',["minmax", "zscore"]),
        "dirPath": dir_path
    }

#ip = sys.argv[1]
#print hyperopt.pyll.stochastic.sample(space)
#finalCountdown random
#finalCountdown_TPE tpe
#key = "final_db"
#db = "db_tpe3"
db = "db_tpe8"
#key = "rand1"
key = "firstTpe"

trials = MongoTrials('mongo://127.0.0.1:27017/'+db+'/jobs', exp_key=key)
#best = fmin(fn=objective, space=spaceCompleteNarrow, trials=trials, algo=hyperopt.random.suggest, max_evals=300000, verbose=1)
best = fmin(fn=objective, space=spaceCompleteNarrow, trials=trials, algo=hyperopt.tpe.suggest, max_evals=300000, verbose=1)
print best
