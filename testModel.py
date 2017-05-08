import json
import modelKeras
import numpy as np
import pandas as pd
import experimentConfig
np.random.seed(1337) # for reproducibility

modelInput = "{}"
#modelInput = '{"optimizer": "adam", "hiddenNodes": 2, "timeWindow": 1, "batchSize": 1, "indexID": 2, "learningRate": 0.001, "epochSize": 10}'
#data=json.loads(modelInput)

c = experimentConfig.Config()
data = c.getBestAsDict("tpe_4", hypeOnly=True)
data2 = c.getBestAsDict("tpe_4")
data["indexID"] = 1
data["isShow"] = True
data["createHTML"] = True

data["showEpochPlots"] = True
data["showKagglePlots"] = True
data["showTrainValPlots"] = True

data["epochSize"] = 2

data["batchSize"] = 50
'''
data["learningRate"] = 0.001
data["standardizationType"] = "zscore"
#data["stationIDs"] = [13,14,15]
data["stationIDs"] = [13]
data["timeWindow"] = 7*24
#data["l1Penalty"] = 0

'''


modelOut = modelKeras.KerasModel(**data)
