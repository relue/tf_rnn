import collections
import random
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
        "stationIDs":True
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

    def generateRandomVektor(self, parameterList):
        dict = {}
        for parameterName in parameterList:
            if self.parameterTypeDiscrete[parameterName]:
                value = random.choice(self.discreteParameterRanges[parameterName])
            else:
                value = random.uniform(self.continousParameterBounds[parameterName][0], self.continousParameterBounds[parameterName][1])
            dict[parameterName] = value
        return dict


