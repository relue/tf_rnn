import json
import modelKeras
import numpy as np
np.random.seed(1337) # for reproducibility
modelInput = "{}"
#modelInput = '{"optimizer": "adam", "hiddenNodes": 2, "timeWindow": 1, "batchSize": 1, "indexID": 2, "learningRate": 0.001, "epochSize": 10}'
data=json.loads(modelInput)
data["indexID"] = 1
data["isShow"] = True
data["createHTML"] = True
data["earlyStopping"] = True
data["epochSize"] = 20
data["batchSize"] = 1
data["learningRate"] = 0.001
data["standardizationType"] = "zscore"
#data["stationIDs"] = [13,14,15]
data["stationIDs"] = [13]
data["timeWindow"] = 7*24


import numpy as np
import pandas as pd

modelOut = modelKeras.KerasModel(**data)
