import numpy as np
import pandas as pd
import os
import sys

dirName= "jobResults/"
dirList = os.listdir(dirName)
dirList.sort()
first = True
dfList = []
errors = []
running = []
results = []
maxAwaiting = sys.argv[1]
for s in dirList:
    name, id = s.split("_")
    if name == "error":
        size = os.stat(dirName+s).st_size
        print s+' has size: '+str(size)
        if size > 3330:
            errors.append(id)
    if name == "output":
        running.append(id)
    if "result" in s:
       dfList.append(pd.read_pickle(dirName+s))
       results.append(id)

result = pd.concat(dfList)
result = result.sort_values(['val_loss'], ascending=[True])

print str(len(errors))+' Fehler in:'
print errors

print str(len(running))+' laufende Jobs'
print str(len(results))+' abgeschlossene Jobs'
print maxAwaiting+ 'jobs geplant'
print result
