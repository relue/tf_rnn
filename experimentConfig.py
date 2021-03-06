import collections
import random
import pandas as pd
'''Umszusetzen:
    - Dropout
    - L1 Penalty
    - Activation Function
'''
class Config():

    parametersAddtionalInput = collections.OrderedDict((
    ("learningRate", [0.001, 0.01, 0.05]),
    ("hiddenLayers"  , [1, 2, 3, 4]),
    ("hiddenNodes" , [10, 32, 50, 128]),
    ("optimizer" , ['adam','sgd']),
    ("timeWindow" , [12, 24, 62,1,128]),
    ("batchSize" , [1,10,30]),
    ("epochSize" , [30,10]),
    ("earlyStopping", [True, False]),
    ("useHoliday" , [True, False]),
    #("useWeekday" , [True, False]),
    ("noFillZero" , [True, False]),
    ("weightInit" , ["one", "glorot_uniform", "lecun_uniform", "glorot_normal"]),
    ("stationIDs" , [[1],[2],[3],[5],[6],[7],[8],[9],[12]]),
    ("cellType", ["lstm", "rnn"]),
    ("standardizationType",["zScore", "minMax"])
    #("activationFunction" , ["tanh", "sigmoid"])
    ))

    parameterTypeDiscrete = {
        "learningRate": False,
        "DropoutProp": False,
        "l1Penalty": False,
        "activationFunction": True,
        "hiddenNodes": True,
        "optimizer": True,
        "timeWindow": True,
        "batchSize": True,
        "hiddenLayers": True,
        "earlyStopping": True,
        "weightInit": True,
        "useHoliday": True,
        "useWeekday": True,
        "noFillZero": True,
        "stationIDs":True,
        "standardizationType":True,
        "epochSize": True,
    }
    parameterNumeric = {
        "hiddenNodes": True,
        "timeWindow": True,
        "batchSize": True,
        "hiddenLayers": True,
        "epochSize": True
    }

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
    experimentConfigWide = {
        'epochSize': range(5, 30),
        "learningRate": (0, 1),
        "DropoutProp": (0, 0.99),
        "l1Penalty": (0, 1),
        "activationFunction": ["tanh", "sigmoid", "relu"],
        "hiddenNodes": range(10, 300),
        "optimizer": ['adam', 'sgd', 'rms', 'ada', 'adadelta'],
        "timeWindow": range(1, 336),
        "batchSize": range(1, 101),
        "hiddenLayers": range(1, 10),
        "weightInit": ["zero", "one", "normal", "glorot_uniform", "lecun_uniform", "glorot_normal"],
        "useHoliday": [True, False],
        "useWeekday": [True, False],
        'standardizationType': ["minmax", "zscore"],
    }
    experimentConfigManual = {
        'epochSize': range(5, 50),
        "learningRate": (0, 0.05),
        "DropoutProp": (0, 0.99),
        "l1Penalty": (0, 0.01),
        "activationFunction": ["tanh", "sigmoid", "relu"],
        "hiddenNodes": range(10, 350),
        "optimizer": ['adam', 'sgd', 'rms', 'ada', 'adadelta'],
        "timeWindow": range(1, 336),
        "batchSize": range(1, 101),
        "hiddenLayers": range(1, 10),
        "weightInit": ["zero", "one", "normal", "glorot_uniform", "lecun_uniform", "glorot_normal"],
        "useHoliday": [True, False],
        "useWeekday": [True, False],
        'standardizationType': ["minmax", "zscore"],
    }
    sensiIntervalsOptimizer = {
        'epochSize': range(1,100),
        "learningRate": (0.0001, 0.02),
        "DropoutProp": (0, 0.99),
        "l1Penalty": (0, 0.00001),
        "activationFunction": ["tanh", "sigmoid", "relu"],
        "hiddenNodes": range(10, 300,5),
        "optimizer": ['adam', 'sgd', 'rms', 'ada', 'adadelta'],
        "timeWindow": range(1, 336),
        "batchSize": range(1, 101,5),
        "hiddenLayers": range(1, 10),
        "weightInit": ["zero", "one", "normal", "glorot_uniform", "lecun_uniform", "glorot_normal"],
        "useHoliday": [True, False],
        "useWeekday": [True, False],
        #"earlyStopping": [True, False],
        'standardizationType': ["minmax", "zscore"]
    }

    defDict = {
        "learningRate":  (0.0001 , 1),
        "DropoutProp": (0.01, 0.99),
        "l1Penalty": (0.0001, 0.99),
        "standardizationType": ["minmax", "zscore"],
        "activationFunction": ["tanh", "sigmoid", "relu"],
        "hiddenNodes": (10,300),
        "optimizer":  ['adam', 'sgd', 'rms','ada', 'adadelta'],
        "timeWindow": (10,199),
        "batchSize": (1,101),
        "hiddenLayers": (1,10),
        "weightInit": ["zero", "one", "normal", "glorot_uniform", "lecun_uniform", "glorot_normal"],
        "useHoliday": [True, False],
        "useWeekday": [True, False],
    }
    data = {}
    data["earlyStopping"] = True
    data["standardizationType"] = "zscore"
    data["stationIDs"] = [13]
    data["noFillZero"] = True
    data["useHoliday"] = True
    data["useWeekday"] = True
    data["indexID"] = 0
    data["epochSize"] = 15
    data["batchSize"] = 1
    data["learningRate"] = 0.001
    data["activationFunction"] = "relu"
    data["l1Penalty"] = 0.000001
    data["DropoutProp"] = 0.001
    data["hiddenNodes"] = 80
    data["hiddenLayers"] = 2
    data["optimizer"] = "adam"
    data["weightInit"] = "lecun_uniform"
    data["timeWindow"] = 7*24

    #data["test_rmse"] = 106159
    #data["val_rmse"] = 15725
    #data["exec_time"] = 600

    def getBestAsDict(self,resultName, hypeOnly = False, orderByIndexID = False):
        df = pd.read_pickle("searchResults/" + resultName + ".pd")

        if orderByIndexID:
            df = df.sort_values(['indexID'], ascending=[True])
        best = df.iloc[0]
        bestD = best.to_dict()
        if hypeOnly:
            nonParameter = ['train_rmse', 'val_rmse', 'test_rmse', 'train_mape', 'val_mape', 'test_mape', 'exec_time']
            if not orderByIndexID:
                hyperOptAdd = ['train_diff', 'val_diff','status', 'train_netrmse', 'loss']
                nonParameter += hyperOptAdd

            for k in nonParameter:
                del bestD[k]
        return bestD

    sensiExperiment1 = data
    def generateRandomVektor(self, parameterList):
        dict = {}
        for parameterName in parameterList:
            if self.parameterTypeDiscrete[parameterName]:
                value = random.choice(self.discreteParameterRanges[parameterName])
            else:
                value = random.uniform(self.continousParameterBounds[parameterName][0], self.continousParameterBounds[parameterName][1])
            dict[parameterName] = value
        return dict


