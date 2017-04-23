#{\"optimizer\": \"adam\", \"hiddenNodes\": 2, \"timeWindow\": 1, \"batchSize\": 1, \"indexID\": 2, \"learningRate\": 0.001, \"epochSize\": 10}
import sys
import json
data=json.loads(sys.argv[1])
verbose=json.loads(sys.argv[2])

if verbose != 1:
    sys.stdout = open('jobResults/output_'+str(data["indexID"]), 'w')
    sys.stderr = open('jobResults/error_'+str(data["indexID"]), 'w')
print sys.argv[1]
print data
import warnings
with warnings.catch_warnings():
    warnings.simplefilter("ignore")
    import modelKeras

    import logging
    import numpy as np
    import pandas as pd
    import time
    start_time = time.time()
    modelOut = modelKeras.KerasModel(**data)

    resultsKeys = ['train_rmse','val_rmse', 'test_rmse', 'train_mape', 'val_mape']
    columns = data.keys() + resultsKeys + ['exec_time']
    for key in resultsKeys:
        data[key] = modelOut.results[key]
    data['exec_time'] = (time.time() - start_time)

    singleResult = pd.DataFrame(data, index=[data["indexID"]])
    singleResult.to_pickle("jobResults/result_"+str(data["indexID"]))
    print singleResult
