import numpy as np
import pandas as pd
import os

dirName= "jobResults/"
dirList = os.listdir(dirName)
dirList.sort()
first = True
dfList = []

for s in dirList:
    if "result" in s:
       dfList.append(pd.read_pickle(dirName+s))

result = pd.concat(dfList)
print result
