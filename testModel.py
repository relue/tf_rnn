import json
import modelKeras

modelInput = "{}"
#modelInput = '{"optimizer": "adam", "hiddenNodes": 2, "timeWindow": 1, "batchSize": 1, "indexID": 2, "learningRate": 0.001, "epochSize": 10}'
data=json.loads(modelInput)
data["indexID"] = 1
data["isShow"] = False
data["createHTML"] = False
data["earlyStopping"] = True
data["epochSize"] = 8
data["learningRate"] = 0.001
data["standardizationType"] = "minmax"
#data["stationIDs"] = [13,14,15]
data["stationIDs"] = [13,14,15]

import numpy as np
import pandas as pd

modelOut = modelKeras.KerasModel(**data)
