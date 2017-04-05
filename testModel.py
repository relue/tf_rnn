import json
import modelKeras

modelInput = "{}"
#modelInput = '{"optimizer": "adam", "hiddenNodes": 2, "timeWindow": 1, "batchSize": 1, "indexID": 2, "learningRate": 0.001, "epochSize": 10}'
data=json.loads(modelInput)
data["indexID"] = 1
data["isShow"] = True
data["createHTML"] = True
data["earlyStopping"] = True
data["epochSize"] = 15

import numpy as np
import pandas as pd

modelOut = modelKeras.KerasModel(**data)
