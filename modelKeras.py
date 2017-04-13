import numpy
import matplotlib.pyplot as plt
import pandas as pd
import math
from keras import regularizers
from keras.models import Sequential
from keras.layers import Dense, Dropout
from keras.layers import LSTM,SimpleRNN
from sklearn.preprocessing import MinMaxScaler, StandardScaler
from sklearn.metrics import mean_squared_error
from bokeh.models import Legend
#import dataExplore2
import imp
import os
dir_path = os.path.dirname(os.path.realpath(__file__))
#import energyload_class
energyload_class = imp.load_source('energyload_class', dir_path +'/energyload_class.py')
callback = imp.load_source('callback',  dir_path +'/callback.py')

import numpy as np
np.random.seed(1337) # for reproducibility
import keras
from bokeh.plotting import figure, show, output_file
from bokeh.models import Legend
from bokeh.io import output_file, show, vplot, gridplot
import itertools
import time



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
            #print "zone"+str(zoneID)+" "+str(math.sqrt((sumZones / counter)))

        error = math.sqrt((sumZones / counter))
        return error

    def getValidationInputOutput(self, df,  stationIDs, timeWindow, scalerOutput, scalerInput, noFillZero = False, useHoliday = True, useWeekday = True, standardizationType="minmax"):
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

        for zone_name in zoneColumns:
            scaledLoads = scalerOutput[zone_name].fit_transform(np.asarray(dfS[zone_name].tolist()).reshape(-1,1))
            lo = pd.Series(scaledLoads.reshape(-1))
            dfS[zone_name] = lo.values

        for station_name in stationColumns:
            scaledTemps = scalerInput[station_name].fit_transform(np.asarray(dfS[station_name].tolist()).reshape(-1,1))
            lo = pd.Series(scaledTemps.reshape(-1))
            dfS[station_name] = lo.values

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

        zoneIDs = zoneIDs
        zoneIDs21= zoneIDs+[21]
        xOutputV = self.getSingleLoadPrediction(tfOutput, zoneIDs21)
        for zoneID in zoneIDs:
            xOutputV[zoneID] = scalerOutput["zone_"+str(zoneID)].inverse_transform(xOutputV[zoneID])

        return tfInput, xOutputV

    def getTestError(self, model, testInput, testOutput, testScalerOutput):
        zoneIDs = range(1,21)
        testPrediction = model.predict(testInput)
        pV = self.getSingleLoadPrediction(testPrediction, zoneIDs)
        pVList = []
        try:
            for zoneID in zoneIDs:
                pV[zoneID] = testScalerOutput["zone_"+str(zoneID)].inverse_transform(pV[zoneID])
                pVList.append(np.asarray(pV[zoneID]))
            pV[21] = np.sum(pVList, axis=0)
            finalTestError = self.calculateKaggleScore(testOutput, pV)
        except ValueError:
            print "scaler out of bounds"
            finalTestError = math.nan

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

    def __init__(self, timeWindow = 24*7,
                   cellType = "rnn",
                   outputSize = 24*7,
                   noFillZero = True,
                   useHoliday = True,
                   useWeekday = True,
                   learningRate = 0.001,
                   l1Penalty = 0.000001,
                   DropoutProp=0.001,
                   hiddenNodes = 30,
                   hiddenLayers = 1,
                   batchSize = 1,
                   epochSize = 20,
                   earlyStopping = True,
                   indexID = 1,
                   optimizer = "adam",
                   stationIDs = [12],
                   validationPercentage = 0.15,
                   weightInit = "lecun_uniform",
                   activationFunction = "tanh",
                   standardizationType = "minmax",
                   isShow = False,
                   createHTML = False):
        optimizerObjects = {
            "sgd" : keras.optimizers.SGD(lr=learningRate, momentum=0.0, decay=0.0, nesterov=False, clipvalue=100),
            "adam" : keras.optimizers.Adam(lr=learningRate, beta_1=0.9, beta_2=0.999, epsilon=1e-08, decay=0.0, clipvalue=100),# empfohlen learning rate default
            "rms" : keras.optimizers.RMSprop(lr=learningRate, rho=0.9, epsilon=1e-08, decay=0.0, clipvalue=100),
            "ada" : keras.optimizers.Adagrad(lr=learningRate, epsilon=1e-08, decay=0.0, clipvalue=100), # empfohlen learning rate default
            "adadelta": keras.optimizers.Adadelta(lr=learningRate, rho=0.95, epsilon=1e-08, decay=0.0, clipvalue=100) # empfohlen learning rate default
        }

        #inputSize = len(stationIDs)+20
        finalOutputSize = outputSize * 20

        df = energyload_class.init_dfs(False, False)

    #
        xInput, xOutput, scalerOutput, scalerInput = energyload_class.createXmulti(df, timeWindow, stationIDs, outputSize, save=False, isStandardized=True, noFillZero=noFillZero, useHoliday=useHoliday, useWeekday=useWeekday, standardizationType=standardizationType)
        xInput = xInput.swapaxes(0,1)
        def getTestSets(xInput, xOutput, percentage):
            fromT = 0
            last = xOutput.shape[0]-1
            toT = int(math.ceil(last*(1-percentage)))
            inputT = xInput[fromT:toT,:]
            outputT = xOutput[fromT:toT,:]
            inputV = xInput[toT+1:last,:]
            outputV = xOutput[toT+1:last,:]
            return inputT, outputT, inputV, outputV
        inputT, outputT, inputV, outputV = getTestSets(xInput, xOutput, validationPercentage)
        inputSize = inputT.shape[2]
        opt = keras.optimizers.SGD(lr=0.1, momentum=0.0, decay=0.0, nesterov=False)
        early = keras.callbacks.EarlyStopping(monitor='loss', min_delta=0, patience=10, verbose=1, mode='auto')
        #shapeInput = [rows, timeSteps, InputSize]
        start_time = time.time()
        model = Sequential()
        returnSequence = True if hiddenLayers > 1 else False
        cellObj = "SimpleRNN" if cellType == "rnn" else "LSTM"

        eval('model.add('+cellObj+'(hiddenNodes, input_length=timeWindow, input_dim=inputSize, '\
                                  'return_sequences=returnSequence, go_backwards = True, init=weightInit, activation=activationFunction))')
#        model.add(LSTM(hiddenNodes, input_length=timeWindow, input_dim=inputSize, return_sequences=returnSequence, go_backwards = True, init=weightInit, activation=activationFunction))
        i = 1
        model.add(Dropout(DropoutProp))
        for hdI in range(2,hiddenLayers+1):
            if hdI == hiddenLayers:
                returnSequence = False
            eval('model.add('+cellObj+'(hiddenNodes, input_length=timeWindow,  return_sequences=returnSequence, '\
             'init=weightInit, activation=activationFunction))')
            #model.add(LSTM(hiddenNodes, input_length=timeWindow, return_sequences=returnSequence, init=weightInit, activation=activationFunction))
            model.add(Dropout(DropoutProp))
        #model.add(SimpleRNN(50, input_length=timeWindow,  return_sequences=False))
        model.add(Dense(finalOutputSize, W_regularizer=regularizers.l1(l1Penalty)))#, kernel_regularizer=regularizers.l1(l1Penalty)

        model.compile(loss='mean_squared_error', optimizer=optimizerObjects[optimizer])
        testInput,testOutput = self.getValidationInputOutput(df, stationIDs, timeWindow, scalerOutput, scalerInput, noFillZero = noFillZero, useHoliday = useHoliday, useWeekday = useWeekday, standardizationType = standardizationType)
        callbacks = []
        if isShow:
            customCallback = callback.KaggleTest(self, testInput,testOutput,scalerOutput)
            callbacks.append(customCallback)
            historyTest = customCallback.getHistory()

        if earlyStopping == False:
            epochSize = 50
            callbacks.append(early)
        history = model.fit(inputT, outputT, nb_epoch=epochSize, batch_size=batchSize, verbose=1, callbacks=callbacks)#callbacks=[early]


        def calulateModelErrors(xInput, xOutput, scalerOutput, model):
            pV, outputV, predList ,outputList = prepareCalculation(xInput, xOutput, scalerOutput, model)
            zoneIDs = range(1,21)
            errorList = []
            errors = {}

            sumP = 0
            sumOutput = 0
            mapeList = []
            try:
                for zoneID in zoneIDs:
                    errorList.append(np.mean((pV[zoneID] - outputV[zoneID]) ** 2))
                    sumP += pV[zoneID]
                    sumOutput += outputV[zoneID]

                errors["rmse"] = np.mean(errorList)** 0.5
                sumP = sum(sumP.reshape(-1))
                sumOutput = sum(sumOutput.reshape(-1))
                errors["diff"] = (sumP - sumOutput) / sumOutput

                for i in range(len(predList)):
                    if outputList[i] != 0:
                        mapeList.append(np.abs((predList[i] - outputList[i]) / outputList[i]))

                errors['mape'] = np.mean(mapeList)
            except ValueError:
                print "scaler out of bounds"
                for d in errors:
                    errors[d] = math.nan
            return errors

        def prepareCalculation(input,output, scaler, model):
            zoneIDs = range(1,21)
            prediction = model.predict(input)
            pV = self.getSingleLoadPrediction(prediction, zoneIDs)
            outputV = self.getSingleLoadPrediction(output, zoneIDs)
            outputList = []
            predList = []
            for zoneID in zoneIDs:
                pV[zoneID] = scaler["zone_"+str(zoneID)].inverse_transform(pV[zoneID])
                outputV[zoneID] = scaler["zone_"+str(zoneID)].inverse_transform(outputV[zoneID])
                outputList.append(outputV[zoneID].reshape(-1))
                predList.append(pV[zoneID].reshape(-1))

            outputList = np.asarray(outputList).reshape(-1)
            predList = np.asarray(predList).reshape(-1)
            return pV,outputV, predList ,outputList


        finalTestError, pV, xOutputV = self.getTestError(model, testInput,testOutput,scalerOutput)


        errorsTrain = calulateModelErrors(inputT, outputT, scalerOutput, model)
        errorsVal = calulateModelErrors(inputV, outputV, scalerOutput, model)
        self.results["train_netrmse"] = history.history['loss'][-1]
        self.results["test_rmse"] = finalTestError
        self.results["train_rmse"] = errorsTrain['rmse']
        self.results["val_rmse"] = errorsVal['rmse']
        self.results["train_mape"] = errorsTrain['mape']
        self.results["val_mape"] = errorsVal['mape']
        self.results["train_diff"] = errorsTrain['diff']
        self.results["val_diff"] = errorsVal['diff']
        self.results["exec_time"] = (time.time() - start_time)
        print  self.results
        for key in errorsTrain:
            print key+" : "+str(errorsTrain[key])+"\n"
        for key in errorsVal:
            print key+" : "+str(errorsVal[key])+"\n"

        print "kaggle:"+str(finalTestError)
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
