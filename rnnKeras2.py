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

inputSize = 2
df = energyload_class.init_dfs(False, False)

df['weekday'] = df['date'].dt.dayofweek
timeWindow = 48

xInput, xOutput, scaler = energyload_class.createXmulti(df, timeWindow, 1, 1, save=True, isStandardized=True)
xInput = xInput.swapaxes(0,1)

opt = keras.optimizers.SGD(lr=0.1, momentum=0.0, decay=0.0, nesterov=False)
early = keras.callbacks.EarlyStopping(monitor='val_loss', min_delta=0, patience=10, verbose=1, mode='auto')
#shapeInput = [rows, timeSteps, InputSize]                               batchSize = batchSize)
model = Sequential()
model.add(SimpleRNN(4, input_length=timeWindow, input_dim=2))
model.add(Dense(24))
model.compile(loss='mean_squared_error', optimizer="adam")
model.fit(xInput, xOutput, nb_epoch=10, batch_size=100, verbose=1, validation_split=0.2, callbacks=[early])
p = model.predict(xInput)

plt.plot(range(0,len(xOutput)),scaler.inverse_transform(p))
plt.plot(range(0,len(xOutput)), scaler.inverse_transform(xOutput))
plt.legend(['p(t)', 'y(t)'], loc='upper left')
plt.show()

