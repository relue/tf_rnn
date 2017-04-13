import hyperopt
from hyperopt import fmin,tpe, hp
from hyperopt.mongoexp import MongoTrials
import socket
import numpy as np
import pandas as pd
import sys
import dataExplore2
with open('logs/ip.log', 'r') as f:
    first_line = f.readline()
ip= first_line
#finalFun
trials = MongoTrials('mongo://'+ip+':27017/foo_db/jobs', exp_key='finalBeta1')
finished = []
for row in trials.results:
    resultRow = row.to_dict()
    if resultRow['status'] == "ok":
        finished.append(resultRow)


dfF = pd.DataFrame(finished)
measures = ["train_netrmse", "test_rmse","train_rmse", "val_rmse", "train_mape", "val_mape","train_diff","val_diff"]
columns = list(dfF)
for m in measures:
    columns.remove(m)
newAlign = measures+columns
dfF = dfF[newAlign]
dfF = dfF.sort_values(['val_rmse'], ascending=[True])
print str(len(finished))+' results collected'
print dfF
dfF.to_pickle("randomSearchResults.pd")
if sys.argv[1] == 1:
    dataExplore2.showDF(dfF, False)

