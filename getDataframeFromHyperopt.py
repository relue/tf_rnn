import hyperopt
from hyperopt import fmin,tpe, hp
from hyperopt.mongoexp import MongoTrials
import socket
import numpy as np
import pandas as pd
import sys

ip= sys.argv[1]
trials = MongoTrials('mongo://'+ip+':27017/foo_db/jobs', exp_key='finalFun')
finished = []
for row in trials.results:
    resultRow = row.to_dict()
    if resultRow['status'] == "ok":
        finished.append(resultRow)

dfF = pd.DataFrame(finished)
print str(len(finished))+' results collected'
print dfF

