import collections

class Config():
    parametersAddtionalInput = collections.OrderedDict((
    ("learningRate", [0.001, 0.01, 0.05]),
    #("hiddenLayer"  , [1, 2, 3, 4]),
    ("hiddenNodes" , [32, 50, 62, 128,256]),
    ("optimizers" , ['adam', 'sgd']),
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
    ("optimizers" , ['adam', 'sgd', 'rms','ada']),
    ("timeWindow" , [1, 12, 24, 36, 48, 96, 144, 120, 168]),
    ("batchSize" , [1,10, 100]),
    ("epochSize" , [30]),
    #("activationFunction" , ["tanh", "sigmoid"])
    ))
