import hyperopt
from hyperopt import fmin,tpe, hp
from hyperopt.mongoexp import MongoTrials
import socket
import numpy as np
import pandas as pd
import sys

ip= sys.argv[1]
#finalFun
trials = MongoTrials('mongo://'+ip+':27017/foo_db/jobs', exp_key='finalAlpha')
finished = []
for row in trials.results:
    resultRow = row.to_dict()
    if resultRow['status'] == "ok":
        finished.append(resultRow)


dfF = pd.DataFrame(finished)

measures = ["loss", "val_loss","test_loss"]
columns = list(dfF)
for m in measures:
    columns.remove(m)
newAlign = measures+columns
dfF = dfF[newAlign]
dfF = dfF.sort_values(['test_loss'], ascending=[True])
print str(len(finished))+' results collected'
print dfF
dfF.to_pickle("randomSearchResults.pd")

