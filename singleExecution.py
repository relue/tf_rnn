#{\"optimizer\": \"adam\", \"hiddenNodes\": 2, \"timeWindow\": 1, \"batchSize\": 1, \"indexID\": 2, \"learningRate\": 0.001, \"epochSize\": 10}
import sys
import json
data=json.loads(sys.argv[1])

sys.stdout = open('jobResults/output_'+str(data["indexID"]), 'w')
sys.stderr = open('jobResults/error_'+str(data["indexID"]), 'w')
print sys.argv[1]
print data
import warnings
with warnings.catch_warnings():
    warnings.simplefilter("ignore")
    import modelKeras
    import time
    import logging
    import numpy as np
    import pandas as pd

    start_time = time.time()
    modelOut = modelKeras.KerasModel(**data)

    data['loss'] = modelOut.results['loss'][-1]
    data['val_loss'] = modelOut.results['val_loss'][-1]
    data['test_loss'] = modelOut.results['test_loss'][-1]
    data['exec_time'] = (time.time() - start_time)
    columns = data.keys() + ['loss', 'val_loss','exec_time']

    singleResult = pd.DataFrame(data, index=[data["indexID"]])
    singleResult.to_pickle("jobResults/result_"+str(data["indexID"]))
    print singleResult
