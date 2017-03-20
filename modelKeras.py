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
import dataExplore2
import energyload_class
import numpy as np
import keras
from bokeh.plotting import figure, show, output_file
from bokeh.models import Legend
from bokeh.io import output_file, show, vplot, gridplot

def validateOriginal():

    return val_loss

def kerasModel(timeWindow = 7*24,
               outputSize = 24,
               learningRate = 0.01,
               hiddenNodes = 2,
               batchSize = 30,
               epochSize = 5,
               indexID = 1,
               optimizer = "adam",
               isShow = False):
    optimizerObjects = {
        "sgd" : keras.optimizers.SGD(lr=learningRate, momentum=0.0, decay=0.0, nesterov=False),
        "adam" : keras.optimizers.Adam(lr=learningRate, beta_1=0.9, beta_2=0.999, epsilon=1e-08, decay=0.0),
    }
    inputSize = 2
    df = energyload_class.init_dfs(False, False)

    df['weekday'] = df['date'].dt.dayofweek
    xInput, xOutput, scaler = energyload_class.createXmulti(df, timeWindow, 1, 1, outputSize, save=False, isStandardized=True)
    xInput = xInput.swapaxes(0,1)

    opt = keras.optimizers.SGD(lr=0.1, momentum=0.0, decay=0.0, nesterov=False)
    early = keras.callbacks.EarlyStopping(monitor='val_loss', min_delta=0, patience=10, verbose=1, mode='auto')
    #shapeInput = [rows, timeSteps, InputSize]
    model = Sequential()
    model.add(SimpleRNN(hiddenNodes, input_length=timeWindow, input_dim=2,  return_sequences=True, go_backwards = False))
    model.add(SimpleRNN(hiddenNodes, input_length=timeWindow,  return_sequences=False))
    #model.add(SimpleRNN(50, input_length=timeWindow,  return_sequences=False))
    model.add(Dense(outputSize))
    model.compile(loss='mean_squared_error', optimizer=optimizerObjects[optimizer])
    history = model.fit(xInput, xOutput, nb_epoch=epochSize, batch_size=batchSize, verbose=1, validation_split=0.1)#callbacks=[early]

    p = model.predict(xInput)
    import itertools
    p = list(itertools.chain(*np.reshape(p,(-1,1))))
    xOutput = list(itertools.chain(*np.reshape(xOutput,(-1,1))))
    p = scaler.inverse_transform(p)
    xOutput = scaler.inverse_transform(xOutput)

    output_file("bokehPlots/modeloutput"+str(indexID)+".html")

    p2 = figure(width=1000, height=500,toolbar_location="left")

    p2.xaxis.axis_label = "Index"
    p2.yaxis.axis_label = "Energy Load "

    r20 = p2.line(range(0,len(xOutput)), xOutput, color="red", line_width=0.5, line_alpha = 0.8)
    r22 = p2.line(range(0,len(xOutput)), p, color="blue", line_width=0.5, line_alpha = 0.8)

    legend2 = Legend(legends=[
        ("Original Data",   [r20]),
        ("Model Prediction", [r22])
    ], location=(40, 5))

    p2.add_layout(legend2, 'below')

    p3 = figure(width=1000, height=500,toolbar_location="left")

    p3.xaxis.axis_label = "Epoch"
    p3.yaxis.axis_label = "Loss"

    r20 = p3.line(range(0,len(xOutput)), history.history['loss'], color="red", line_width=1, line_alpha = 0.8)
    r22 = p3.line(range(0,len(xOutput)), history.history['val_loss'], color="blue", line_width=1, line_alpha = 0.8)

    legend2 = Legend(legends=[
        ("Loss Training",   [r20]),
        ("Loss Validation", [r22])
    ], location=(40, 5))

    p3.add_layout(legend2, 'below')

    ap = gridplot([[p2],[p3]])
    if isShow:
        show(ap)
    return history

#kerasModel(isShow = True)
