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
missing = []

for s in dirList:
    name, id = s.split("_")
    id = int(id)
    if name == "error":
        size = os.stat(dirName+s).st_size
        if size > 3330:
            errors.append(id)
    if name == "output":
        running.append(id)
    if "result" in s:
        size = os.stat(dirName+s).st_size
        if size > 5:
           dfList.append(pd.read_pickle(dirName+s))
           results.append(id)

result = pd.concat(dfList)
result = result.sort_values(['val_loss'], ascending=[True])

maxAwaiting = max(running)
for i in range(0, int(maxAwaiting)):
    if i not in results:
        missing.append(i)
print str(len(errors))+' Fehler in:'
print errors

print str(len(running))+' laufende Jobs'
print str(len(results))+' abgeschlossene Jobs'
print str(maxAwaiting)+ 'jobs geplant'
print "fehlende id's:"
print missing
print result
