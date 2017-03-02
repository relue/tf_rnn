import numpy
import matplotlib.pyplot as plt
import pandas
import math
from keras.models import Sequential
from keras.layers import Dense
from keras.layers import LSTM,SimpleRNN
from sklearn.preprocessing import MinMaxScaler
from sklearn.metrics import mean_squared_error
import energyload_class
import numpy as np
import keras

zone_id = "zone_1"
featureList = ["zone_1"]
inputSize = len(featureList)
df = energyload_class.init_dfs(False, False)
df['weekday'] = df['date'].dt.dayofweek
timeWindow = 1

xInput, xOutput = energyload_class.createX(df, featureList, save=False, isMLP = False, isLogarithmic=False,
                                           timeWindow = timeWindow, jumpSequences = False)
xInput = xInput.swapaxes(0,1)

opt = keras.optimizers.SGD(lr=0.1, momentum=0.0, decay=0.0, nesterov=False)
#shapeInput = [rows, timeSteps, InputSize]                               batchSize = batchSize)
model = Sequential()
model.add(SimpleRNN(4, input_length=timeWindow, input_dim=1))
model.add(Dense(1))
model.compile(loss='mean_squared_error', optimizer=opt)
model.fit(xInput, xOutput, nb_epoch=50, batch_size=32, verbose=1)
p = model.predict(xInput)



# model = Sequential()
# model.add(Dense(1, input_dim=1, init='glorot_normal'))
# model.add(Dense(1, init='glorot_normal'))
# model.compile(loss='mean_squared_error', optimizer=opt)
# model.fit(xInput, xOutput, nb_epoch=20, batch_size=100, verbose=1)
# p = model.predict(xInput)

plt.plot(range(0,len(xOutput)),p)
plt.plot(range(0,len(xOutput)), xOutput)
plt.legend(['p(t)', 'y(t)'], loc='upper left')
plt.show()
