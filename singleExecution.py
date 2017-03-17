#{\"optimizer\": \"adam\", \"hiddenNodes\": 2, \"timeWindow\": 1, \"batchSize\": 1, \"indexID\": 2, \"learningRate\": 0.001, \"epochSize\": 10}
import sys
import json
data=json.loads(sys.argv[1])
sys.stdout = open('jobResults/output'+str(data["indexID"]), 'w')
sys.err = open('jobResults/error'+str(data["indexID"]), 'w')
import modelKeras

import time
import logging
import numpy as np
import pandas as pd

start_time = time.time()
modelOut = modelKeras.kerasModel(**data)
data['loss'] = modelOut.history['loss'][-1]
data['val_loss'] = modelOut.history['val_loss'][-1]
data['exec_time'] = (time.time() - start_time)
columns = data.keys() + ['loss', 'val_loss','exec_time']

singleResult = pd.DataFrame(data, index=[data["indexID"]])
singleResult.to_pickle("jobResults/result"+str(data["indexID"]))
print singleResult
