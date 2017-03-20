#{\"optimizer\": \"adam\", \"hiddenNodes\": 2, \"timeWindow\": 1, \"batchSize\": 1, \"indexID\": 2, \"learningRate\": 0.001, \"epochSize\": 10}
import sys
import json
data=json.loads(sys.argv[1])
print sys.argv[1]
print data
sys.stdout = open('jobResults/output_'+str(data["indexID"]), 'w')
sys.stderr = open('jobResults/error_'+str(data["indexID"]), 'w')

import warnings
with warnings.catch_warnings():
    warnings.simplefilter("ignore")
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
    singleResult.to_pickle("jobResults/result_"+str(data["indexID"]))
    print singleResult
