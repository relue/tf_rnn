import collections

'''Umszusetzen:
    - Dropout
    - L1 Penalty
    - Activation Function
'''
class Config():

    parametersAddtionalInput = collections.OrderedDict((
    ("learningRate", [0.001, 0.01, 0.05]),
    #("hiddenLayer"  , [1, 2, 3, 4]),
    ("hiddenNodes" , [32, 50, 62, 128,256]),
    ("optimizer" , ['adam']),
    ("timeWindow" , [12, 24, 36]),
    ("batchSize" , [1,10]),
    ("epochSize" , [30]),
    ("useHoliday" , [True, False]),
    ("useWeekday" , [True, False]),
    ("noFillZero" , [True, False])
    #("activationFunction" , ["tanh", "sigmoid"])
    ))

    standardParamater = collections.OrderedDict((
    ("learningRate", [0.001, 0.01, 0.05, 0.1, 0.2]),
    #("hiddenLayer"  , [1, 2, 3, 4]),
    ("hiddenNodes" , [2, 4, 8, 16, 32, 50, 62, 128,256]),
    ("optimizer" , ['adam', 'sgd', 'rms','ada']),
    ("timeWindow" , [1, 12, 24, 36, 48, 96, 144, 120, 168]),
    ("batchSize" , [1,10, 100]),
    ("epochSize" , [30]),
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
        "weightInit": True
    }

    continousParameterBounds = {
        "learningRate": (0,1),
        "DropoutProp": (0,1),
        "l1Penalty": (0,1)
    }

    discreteParameterRanges = {
        "activationFunction": ["hypT", "Sig", "Relu"],
        "hiddenNodes": range(10,1001),
        "optimizer": ['adam', 'sgd', 'rms','ada', 'adadelta'],
        "timeWindow": range(10,137),
        "batchSize": range(1,101),
        "hiddenLayers": range(1,11),
        "weightInit": ["zero", "one", "normal", "glorot_uniform", "lecun_uniform", "glorot_normal"]
    }

    def generateRandom(self):
        return 0


