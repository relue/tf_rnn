import numpy
import matplotlib.pyplot as plt
import pandas
import math
from keras.models import Sequential
from keras.layers import Dense
from keras.layers import LSTM,SimpleRNN
from sklearn.preprocessing import MinMaxScaler
from sklearn.metrics import mean_squared_error
from bokeh.models import Legend

import energyload_class
import numpy as np
import keras
from bokeh.plotting import figure, show, output_file
from bokeh.models import Legend

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
model.add(SimpleRNN(100, input_length=timeWindow, input_dim=2))
model.add(Dense(24))
model.compile(loss='mean_squared_error', optimizer="adam")
model.fit(xInput, xOutput, nb_epoch=200, batch_size=10, verbose=1, validation_split=0.1)#callbacks=[early]
p = model.predict(xInput)
import itertools
p = list(itertools.chain(*np.reshape(p,(-1,1))))
xOutput = list(itertools.chain(*np.reshape(xOutput,(-1,1))))
p = scaler.inverse_transform(p)
xOutput = scaler.inverse_transform(xOutput)

output_file("model.html")

p2 = figure(width=1000, height=500,toolbar_location="left")

p2.xaxis.axis_label = "Index"
p2.yaxis.axis_label = "Engery Load "

r20 = p2.line(range(0,len(xOutput)), xOutput, color="red", line_width=0.5, line_alpha = 0.8)
r22 = p2.line(range(0,len(xOutput)), p, color="blue", line_width=0.5, line_alpha = 0.8)

legend2 = Legend(legends=[
    ("Original Data",   [r20]),
    ("Model Prediction", [r22])
], location=(40, 5))

p2.add_layout(legend2, 'below')
show(p2)

#plt.plot(range(0,len(xOutput)),p) #
#plt.plot(range(0,len(xOutput)), xOutput)
#plt.legend(['p(t)', 'y(t)'], loc='upper left')
#plt.show()

