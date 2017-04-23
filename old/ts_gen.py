
import tensorflow as tf
import numpy as np
import random
import matplotlib.pyplot as plt
from itertools import repeat

import math
'''
Erezuge eine Zeitreihe im Format

x1;x2;x3;n1;y1

wobei

x1, x2, x3 Zufallswerte zwischen 5 und 10
y = x1 + x2 + x3 + n1
'''

rows = 100

def generate_ts(rows, isTransform = False):
    listA = []
    listNew = []
    a = []
    random.seed(1234)

    for i in range(0, rows):
        x1 = abs(round(random.gauss(500, 80), 1))
        x2 = abs(round(random.gauss(20, 20), 1))
        x3 = abs(round(random.gauss(10, 10), 1))

        y = abs(round(random.gauss(500, 5), 1))
        n1 = round(random.gauss(30, 3), 1)

        '''
        Y ergibt sich aus x1,x2,x3 direkt im aktuellen Zeitschritt
        '''
        if i > 1:
            y_next= x1 + x2
        else:
            y_next= y

        #a = [x1, x2, y_next]
        if isTransform:
            x1 = math.log1p(x1)
            x2 = math.log1p(x2)
            x3 = math.log1p(x3)
            y_next = math.log1p(y_next)
        a = [x1, x2, y_next]
        listA.append(a)

    ar = np.array (listA)
    return ar

def createInput(dataX, timeWindow, xDimensions):
    listNew = []
    spaceMul = xDimensions*(timeWindow+1)
    for i in range(0, len(dataX)):
        if i > timeWindow-1:
            begin = i-timeWindow
            row = dataX[begin:i+1,:]
            row = np.reshape(row, spaceMul)
        else:
            row = dataX[i,:]
            row = row.tolist() + list(repeat(0,spaceMul-xDimensions))
        listNew.append(row)

    ar = np.array (listNew)
    return ar

def getBatch(dataX, batch_i, batches):
    batch_size = batches
    stepSize = len(dataX)/batches
    begin = batch_i*stepSize-stepSize
    end = begin+stepSize
    if dataX.ndim > 1:
        return dataX[begin:end,:]
    else:
        return dataX[begin:end]

