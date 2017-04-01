import numpy
import matplotlib.pyplot as plt
import pandas as pd
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
np.random.seed(1337) # for reproducibility
import keras
from bokeh.plotting import figure, show, output_file
from bokeh.models import Legend
from bokeh.io import output_file, show, vplot, gridplot
import itertools
from callback import KaggleTest

class KerasModel():
    results = {}
    def calculateKaggleScore(self, xOutputV, pV):
        zoneIDs = range(1,21)
        sumZones = 0
        counter = 0
        zoneIDs.append(21)

        for zoneID in zoneIDs:
            if zoneID == 21:
                weightZone= 20
            else:
                weightZone = 1
            for valWeek in range(len(xOutputV[zoneID])):
                if valWeek == 8:
                    finalWeight = weightZone*8
                else:
                    finalWeight = weightZone
                #finalWeight = 1
                for hour in range(len(xOutputV[zoneID][valWeek])):
                    sumZones += ((xOutputV[zoneID][valWeek][hour] - pV[zoneID][valWeek][hour]) ** 2)*finalWeight
                    counter += 1*finalWeight

        error = math.sqrt((sumZones / counter))
        return error

    def getValidationInputOutput(self, df,  stationIDs, timeWindow, noFillZero = False, useHoliday = True, useWeekday = True):
        backcastWeeks = ["2005-3-5", "2005-6-19", "2005-9-9", "2005-12-24",
                                 "2006-2-12", "2006-5-24", "2006-8-1", "2006-11-21","2008-6-30"]
        columns = range(1, timeWindow+1)
        zoneIDs = range(1,21)
        zoneColumns = ["zone_" + str(i) for i in zoneIDs]
        stationColumns = ["station_" + str(i) for i in stationIDs]
        dfNew = pd.DataFrame(columns=columns)
        df['weekday'] = df['date'].dt.dayofweek
        dfS = df[zoneColumns+stationColumns+["zone_21"]+["date", "weekday"]]
        dfS = dfS.fillna(0)
        dfDummy = pd.get_dummies(dfS['weekday'])
        dfS = pd.concat([dfS, dfDummy], axis=1)
        holidayDict = energyload_class.getHolidayDict()
        scalerInput = MinMaxScaler(feature_range=(0, 1))
        scalerOutput = MinMaxScaler(feature_range=(0, 1))
        scalerOutputZone21 = MinMaxScaler(feature_range=(0, 1))

        #dataExplore2.showDF(df, False)
        for zone_name in zoneColumns:
            scaledLoads = scalerOutput.fit_transform(dfS[zone_name].tolist())
            lo = pd.Series(scaledLoads)
            dfS[zone_name] = lo.values

        for station_name in stationColumns:
            scaledTemps = scalerInput.fit_transform(dfS[station_name].tolist())
            lo = pd.Series(scaledTemps)
            dfS[station_name] = lo.values

        #Eigene Transformation for Zone 21
        scaledLoads = scalerOutputZone21.fit_transform(dfS["zone_21"].tolist())
        lo = pd.Series(scaledLoads)
        dfS["zone_21"] = lo.values

        for date in backcastWeeks:
            mask = (df['date'] == date)
            i = df.loc[mask].index[0]+24
            row = energyload_class.createInputOutputRow(dfS, i, columns, zoneColumns, stationColumns, 7*24, holidayDict, addSystemLevel = True, noFillZero=noFillZero, useHoliday=useHoliday, useWeekday=useWeekday)
            dfNew = dfNew.append([row],ignore_index=True)

        #dataExplore2.showDF(dfNew, False)
        tfOutput = np.asarray(dfNew["output"].tolist())
        tfInput = []
        for t in columns:
            tfInput.append(dfNew[t].tolist())
        tfInput= np.asarray(tfInput)

        tfInput = tfInput.swapaxes(0,1)

        zoneIDs = zoneIDs+[21]
        xOutputV = self.getSingleLoadPrediction(tfOutput, zoneIDs)
        for zoneID in zoneIDs:
            if zoneID == 21:
                xOutputV[zoneID] = scalerOutputZone21.inverse_transform(xOutputV[zoneID])
            else:
                xOutputV[zoneID] = scalerOutput.inverse_transform(xOutputV[zoneID])

        return tfInput, xOutputV, scalerOutput

    def getTestError(self, model, testInput, testOutput, testScalerOutput):
        zoneIDs = range(1,21)
        testPrediction = model.predict(testInput)
        testPrediction = testScalerOutput.inverse_transform(testPrediction)
        pV = self.getSingleLoadPrediction(testPrediction, zoneIDs)
        pVList = []
        for zoneID in zoneIDs:
                pVList.append(np.asarray(pV[zoneID]))
        pV[21] = np.sum(pVList, axis=0)
        finalTestError = self.calculateKaggleScore(testOutput, pV)
        return finalTestError, pV, testOutput

    def getSingleLoadPrediction(self, outputArray, zoneIDs):
        sequenceLoads = {}
        for zoneID in zoneIDs:
            sequenceLoads[zoneID] = []
            for row in outputArray:
                column = []
                for i in range(zoneID-1, len(row), len(zoneIDs)):
                    column.append(row[i])
                sequenceLoads[zoneID].append(column)
        return sequenceLoads

    def __init__(self, timeWindow = 24*2,
                   outputSize = 24*7,
                   noFillZero = False,
                   useHoliday = False,
                   useWeekday = True,
                   learningRate = 0.001,
                   l1Penalty = 0.01,
                   DropoutProp=0.01,
                   hiddenNodes = 40,
                   hiddenLayers = 1,
                   batchSize = 1,
                   epochSize = 20,
                   earlyStopping = True,
                   indexID = 1,
                   optimizer = "adam",
                   isShow = False,
                   stationIDs = [12],
                   weightInit = "lecun_uniform",
                   activationFunction = "tanh",
                   createHTML = False):
        optimizerObjects = {
            "sgd" : keras.optimizers.SGD(lr=learningRate, momentum=0.0, decay=0.0, nesterov=False),
            "adam" : keras.optimizers.Adam(lr=0.001, beta_1=0.9, beta_2=0.999, epsilon=1e-08, decay=0.0),# empfohlen learning rate default
            "rms" : keras.optimizers.RMSprop(lr=learningRate, rho=0.9, epsilon=1e-08, decay=0.0),
            "ada" : keras.optimizers.Adagrad(lr=0.01, epsilon=1e-08, decay=0.0), # empfohlen learning rate default
            "adadelta": keras.optimizers.Adadelta(lr=1.0, rho=0.95, epsilon=1e-08, decay=0.0) # empfohlen learning rate default
        }

        #inputSize = len(stationIDs)+20
        finalOutputSize = outputSize * 20

        df = energyload_class.init_dfs(False, False)

    #
        xInput, xOutput, scaler = energyload_class.createXmulti(df, timeWindow, stationIDs, outputSize, save=False, isStandardized=True, noFillZero=noFillZero, useHoliday=useHoliday, useWeekday=useWeekday)
        xInput = xInput.swapaxes(0,1)
        inputSize = xInput.shape[2]
        opt = keras.optimizers.SGD(lr=0.1, momentum=0.0, decay=0.0, nesterov=False)
        early = keras.callbacks.EarlyStopping(monitor='val_loss', min_delta=0, patience=20, verbose=1, mode='auto')
        #shapeInput = [rows, timeSteps, InputSize]
        model = Sequential()
        returnSequence = True if hiddenLayers > 1 else False
        model.add(SimpleRNN(hiddenNodes, input_length=timeWindow, input_dim=inputSize,  return_sequences=returnSequence, go_backwards = True, init=weightInit, activation=activationFunction))
        i = 1
        for hdI in range(2,hiddenLayers+1):
            if hdI == hiddenLayers:
                returnSequence = False
            model.add(SimpleRNN(hiddenNodes, input_length=timeWindow,  return_sequences=returnSequence, init=weightInit, activation=activationFunction))
        #model.add(SimpleRNN(50, input_length=timeWindow,  return_sequences=False))
        model.add(Dense(finalOutputSize))
        model.compile(loss='mean_squared_error', optimizer=optimizerObjects[optimizer])
        testInput,testOutput,testScaler = self.getValidationInputOutput(df, stationIDs, timeWindow, noFillZero = noFillZero, useHoliday = useHoliday, useWeekday = useWeekday)
        customCallback = KaggleTest(self, testInput,testOutput,testScaler)
        callbacks = [].append(customCallback)
        if not earlyStopping:
            epochSize = 100
            callbacks.append(early)
        history = model.fit(xInput, xOutput, nb_epoch=epochSize, batch_size=batchSize, verbose=1, validation_split=0.3, callbacks=callbacks)#callbacks=[early]
        historyTest = customCallback.getHistory()
        self.results["loss"] = history.history['loss']
        self.results["val_loss"] = history.history['val_loss']
        self.results["test_loss"] = historyTest
        finalTestError, pV, xOutputV = self.getTestError(model, testInput,testOutput,testScaler)
        print "final Test Error: "+str(finalTestError)
        if createHTML:
            p3 = figure(width=1000, height=500,toolbar_location="left")

            p3.xaxis.axis_label = "Epoch"
            p3.yaxis.axis_label = "Loss"

            r20 = p3.line(range(0,len(xOutput)), history.history['loss'], color="red", line_width=1, line_alpha = 0.8)
            r22 = p3.line(range(0,len(xOutput)), history.history['val_loss'], color="blue", line_width=1, line_alpha = 0.8)

            legend2 = Legend(legends=[
                ("Loss Training Set",   [r20]),
                ("Loss Validation Set", [r22])
            ], location=(40, 5))

            p3.add_layout(legend2, 'below')

            p2 = figure(width=1000, height=500,toolbar_location="left")

            p2.xaxis.axis_label = "Epoch"
            p2.yaxis.axis_label = "Loss"

            r23 = p2.line(range(0,len(xOutput)), historyTest, color="green", line_width=1, line_alpha = 0.8)

            legend2 = Legend(legends=[
                ("Loss Test Set", [r23])
            ], location=(40, 5))

            p2.add_layout(legend2, 'below')

            #p = model.predict(xInput)
            #xOutputV = getSingleLoadPrediction(xOutput)
            #pV = getSingleLoadPrediction(p)

            zonePlots = {}

            zoneIDs = range(1,22)
            for zoneID in zoneIDs:
                p = list(itertools.chain(*np.reshape(pV[zoneID],(-1,1))))
                xOutput = list(itertools.chain(*np.reshape(xOutputV[zoneID],(-1,1))))
                #p = scaler.inverse_transform(p)
                #xOutput = scaler.inverse_transform(xOutput)

                output_file("bokehPlots/modeloutput"+str(indexID)+".html")

                zonePlots[zoneID] = figure(width=1000, height=500,toolbar_location="left", title="Zone "+str(zoneID))

                zonePlots[zoneID].xaxis.axis_label = "Index"
                zonePlots[zoneID].yaxis.axis_label = "Energy Load "

                r20 = zonePlots[zoneID].line(range(0,len(xOutput)), xOutput, color="red", line_width=0.5, line_alpha = 0.8)
                r22 = zonePlots[zoneID].line(range(0,len(xOutput)), p, color="blue", line_width=0.5, line_alpha = 0.8)


                legend2 = Legend(legends=[
                    ("Original Data",   [r20]),
                    ("Model Prediction", [r22])
                ], location=(40, 5))

                zonePlots[zoneID].add_layout(legend2, 'below')

            zoneGrid = [zonePlots[i] for i in range(1,22)]
            zoneGrid = [p2] + [p3] + zoneGrid

            from bokeh.layouts import column
            ap = column(zoneGrid)
            if isShow:
                show(ap)

#KerasModel(isShow= True, createHTML= True)
