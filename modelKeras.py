import numpy
import pandas as pd
import math
from keras import regularizers
from keras.models import Sequential
from keras.layers import Dense, Dropout
from keras.layers import LSTM,SimpleRNN

#import dataExplore2
import imp
import os
dir_path = os.path.dirname(os.path.realpath(__file__))
#import energyload_class
energyload_class = imp.load_source('energyload_class', dir_path +'/energyload_class.py')
callback = imp.load_source('callback',  dir_path +'/callback.py')

import numpy as np
from random import shuffle
np.random.seed(1337) # for reproducibility
import keras
from bokeh.plotting import figure, show, output_file
from bokeh.models import Legend
from bokeh.io import output_file, show, vplot, gridplot
import itertools
import time

class KerasModel():
    results = {}

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
               hiddenLayers = 2,
               batchSize = 1,
               epochSize = 30,
               earlyStopping = True,
               indexID = 1,
               optimizer = "adam",
               stationIDs = [13],
               validationPercentage = 0.20,
               testPercentage = 0.20,
               weightInit = "lecun_uniform",
               activationFunction = "tanh",
               standardizationType = "zscore",
               isShow = False,
               createHTML = False,
               showEpochPlots = False,
               showKagglePlots = False,
               showTrainValPlots = False,
                 ):
        optimizerObjects = {
            "sgd" : keras.optimizers.SGD(lr=learningRate, momentum=0.0, decay=0.0, nesterov=False, clipvalue=100),
            "adam" : keras.optimizers.Adam(lr=learningRate, beta_1=0.9, beta_2=0.999, epsilon=1e-08, decay=0.0, clipvalue=100),# empfohlen learning rate default
            "rms" : keras.optimizers.RMSprop(lr=learningRate, rho=0.9, epsilon=1e-08, decay=0.0, clipvalue=100),
            "ada" : keras.optimizers.Adagrad(lr=learningRate, epsilon=1e-08, decay=0.0, clipvalue=100), # empfohlen learning rate default
            "adadelta": keras.optimizers.Adadelta(lr=learningRate, rho=0.95, epsilon=1e-08, decay=0.0, clipvalue=100) # empfohlen learning rate default
        }

        finalOutputSize = outputSize * 20
        start_time = time.time()

        xInput, xOutput, scalerOutput, scalerInput, dfS = energyload_class.createXmulti(timeWindow, stationIDs, outputSize, save=False, isStandardized=True, noFillZero=noFillZero, useHoliday=useHoliday, useWeekday=useWeekday, standardizationType=standardizationType)
        xInput = xInput.swapaxes(0,1)


        #xInput,xOutput = self.shuffleData(xInput, xOutput)

        inputT, outputT, inputB, outputB = self.getTestSets(xInput, xOutput, validationPercentage+testPercentage)
        inputV, outputV, inputV2, outputV2 = self.getTestSets(inputB, outputB, testPercentage/(validationPercentage+testPercentage))
        inputSize = inputT.shape[2]
        early = keras.callbacks.EarlyStopping(monitor='val_loss', min_delta=0, patience=10, verbose=2, mode='auto')
        start_time = time.time()
        model = Sequential()
        returnSequence = True if hiddenLayers > 1 else False
        cellObj = "SimpleRNN" if cellType == "rnn" else "LSTM"
        eval('model.add('+cellObj+'(hiddenNodes, input_length=timeWindow, input_dim=inputSize, '\
                                  'return_sequences=returnSequence, go_backwards = True, init=weightInit, activation=activationFunction))')
        i = 1
        model.add(Dropout(DropoutProp))
        for hdI in range(2,hiddenLayers+1):
            if hdI == hiddenLayers:
                returnSequence = False
            eval('model.add('+cellObj+'(hiddenNodes, input_length=timeWindow, go_backwards = False, return_sequences=returnSequence, '\
             'init=weightInit, activation=activationFunction))')

            model.add(Dropout(DropoutProp))

        model.add(Dense(finalOutputSize, W_regularizer=regularizers.l1(l1Penalty)))#, kernel_regularizer=regularizers.l1(l1Penalty)

        model.compile(loss='mean_squared_error', optimizer=optimizerObjects[optimizer])
        testInput,testOutput = self.getValidationInputOutput(stationIDs, timeWindow, scalerOutput, scalerInput, dfS,
                                                             noFillZero = noFillZero, useHoliday = useHoliday, useWeekday = useWeekday,
                                                             standardizationType = standardizationType)
        callbacks = []
        if showEpochPlots:
            customCallback = callback.EpochErrorRetrieve(self, testInput,testOutput, inputT, outputT,
                                                         inputV, outputV, inputV2, outputV2, scalerOutput)
            callbacks.append(customCallback)
            #historyTest = customCallback.getHistory()

        if earlyStopping == False:
            epochSize = 50
            callbacks.append(early)
        history = model.fit(inputT, outputT,  nb_epoch=epochSize, batch_size=batchSize, verbose=0, callbacks=callbacks)#callbacks=[early]
        #validation_data = (inputV, outputV),
        #finalTestError, test_pV, test_xOutputV = self.getTestError(model, testInput,testOutput,scalerOutput)
        errorsTrain, train_pV, train_xOutputV = self.calulateModelErrors(inputT, outputT, scalerOutput, model)
        errorsVal, val_pV, val_xOutputV = self.calulateModelErrors(inputV, outputV, scalerOutput, model)
        errorsTest, test_pV, test_xOutputV = self.calulateModelErrors(inputV2, outputV2, scalerOutput, model)

        self.results["train_netrmse"] = history.history['loss'][-1]
        self.results["test_rmse"] = errorsTest['rmse']
        self.results["test_mape"] = errorsTest['mape']
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
        for key in errorsTest:
            print key+" : "+str(errorsTest[key])+"\n"

        #print "kaggle:"+str(finalTestError)
        print "test 3 "+str((time.time() - start_time))
        if createHTML:
            plots = []

            if showEpochPlots:
                epochPlots = self.getEpochPlots(customCallback)
                output_file("bokehPlots/epochs.html")
                #plots += epochPlots
                grid = [[plot] for plot in epochPlots]
                ap = gridplot(grid)
                if isShow:
                    show(ap)
            '''
            if showKagglePlots:
                kagglePlots = self.getKagglePlots(test_pV, test_xOutputV)
                output_file("bokehPlots/kaggleTest" + str(indexID) + ".html")
                grid = [[plot] for plot in kagglePlots]
                ap = gridplot(grid)
                if isShow:
                    show(ap)
            '''

            if showTrainValPlots:
                output_file("bokehPlots/trainValPlot" + str(indexID) + ".html")
                trainValPlots = self.getTrainValPlots(train_pV, train_xOutputV, val_pV, val_xOutputV, test_pV, test_xOutputV)
                #plots += trainValPlots
                grid = [[plot] for plot in trainValPlots]
                ap = gridplot(grid)
                if isShow:
                    show(ap)

            from bokeh.layouts import column
            grid = [[plot] for plot in plots]
            ap = gridplot(grid)

    def shuffleData(self, xInput, xOutput):
        xInputShuf = []
        xOutputShuf = []
        index_shuf = range(len(xInput))
        shuffle(index_shuf)
        for i in index_shuf:
            xInputShuf.append(xInput[i])
            xOutputShuf.append(xOutput[i])
        return np.asarray(xInputShuf), np.asarray(xOutputShuf)

    def getLinePlot(self, pV, xOutputV, zoneID, title):
        p = figure(width=1000, height=500, toolbar_location="left", title=title+" - Zone " + str(zoneID))

        p.xaxis.axis_label = "Index"
        p.yaxis.axis_label = "Energy Load"

        r20 = p.line(range(0, len(xOutputV)), xOutputV, color="red", line_width=0.5, line_alpha=0.8)
        r22 = p.line(range(0, len(xOutputV)), pV, color="blue", line_width=0.5, line_alpha=0.8)

        legend2 = Legend(legends=[
            ("Original Data", [r20]),
            ("Model Prediction", [r22])
        ], location=(40, 5))
        p.add_layout(legend2, 'below')
        return p

    def getJumps(self, arr, jump):
        i = 0
        n = 0
        newVec = []
        for v in range(0, arr.shape[0],jump):
            newVec.append(arr[v])

        return newVec

    def getTrainValPlots(self,train_pV, train_xOutputV, val_pV, val_xOutputV, test_pV, test_xOutputV, jump=24):
        zonePlots = {}

        zoneIDs = range(1, 21)
        zoneList = []
        for zoneID in zoneIDs:
            jumpedP = self.getJumps(train_pV[zoneID], jump)
            jumpedO = self.getJumps(train_xOutputV[zoneID], jump)
            train_p = list(itertools.chain(*np.reshape(jumpedP, (-1, 1))))
            train_xOutput = list(itertools.chain(*np.reshape(jumpedO, (-1, 1))))

            p = self.getLinePlot(train_p, train_xOutput, zoneID, "Train Dataset")
            zoneList.append(p)

            jumpedP = self.getJumps(val_pV[zoneID], jump)
            jumpedO = self.getJumps(val_xOutputV[zoneID], jump)
            val_p = list(itertools.chain(*np.reshape(jumpedP, (-1, 1))))
            val_xOutput = list(itertools.chain(*np.reshape(jumpedO, (-1, 1))))

            p = self.getLinePlot(val_p, val_xOutput, zoneID, "Validation Dataset")
            zoneList.append(p)

            jumpedP = self.getJumps(test_pV[zoneID], jump)
            jumpedO = self.getJumps(test_xOutputV[zoneID], jump)
            test_p = list(itertools.chain(*np.reshape(jumpedP, (-1, 1))))
            test_xOutput = list(itertools.chain(*np.reshape(jumpedO, (-1, 1))))

            p = self.getLinePlot(test_p, test_xOutput, zoneID, "Test Dataset")
            zoneList.append(p)
        return zoneList

    def getKagglePlots(self, pV, xOutputV):
        zonePlots = {}

        zoneIDs = range(1, 22)
        for zoneID in zoneIDs:
            p = list(itertools.chain(*np.reshape(pV[zoneID], (-1, 1))))
            xOutput = list(itertools.chain(*np.reshape(xOutputV[zoneID], (-1, 1))))
            # p = scaler.inverse_transform(p)
            # xOutput = scaler.inverse_transform(xOutput)


            zonePlots[zoneID] = figure(width=1000, height=500, toolbar_location="left", title="Zone " + str(zoneID))

            zonePlots[zoneID].xaxis.axis_label = "Index"
            zonePlots[zoneID].yaxis.axis_label = "Energy Load "

            r20 = zonePlots[zoneID].line(range(0, len(xOutput)), xOutput, color="red", line_width=0.5, line_alpha=0.8)
            r22 = zonePlots[zoneID].line(range(0, len(xOutput)), p, color="blue", line_width=0.5, line_alpha=0.8)

            legend2 = Legend(legends=[
                ("Original Data", [r20]),
                ("Model Prediction", [r22])
            ], location=(40, 5))
            zonePlots[zoneID].add_layout(legend2, 'below')
        zoneList = [zonePlots[i] for i in range(1, 22)]
        return zoneList
        #
    def getEpochPlots(self, customCallback):
        testErrors, trainErrors, valErrors = customCallback.getErrors()
        epochPlots = []
        p3 = figure(width=1000, height=500, toolbar_location="left")
        p3.xaxis.axis_label = "Epoch"
        p3.yaxis.axis_label = "Loss"
        r20 = p3.line(range(0, len(trainErrors['rmse'])), trainErrors['rmse'], color="red", line_width=1, line_alpha=0.8)
        r22 = p3.line(range(0, len(trainErrors['rmse'])), valErrors['rmse'], color="blue", line_width=1, line_alpha=0.8)
        r23 = p3.line(range(0, len(trainErrors['rmse'])), testErrors['rmse'], color="green", line_width=1, line_alpha=0.8)
        legend2 = Legend(legends=[
            ("RMSE Training Set", [r20]),
            ("RMSE Validation Set", [r22]),
            ("RMSE Test Set", [r23])
        ], location=(40, 5))
        p3.add_layout(legend2, 'below')
        epochPlots.append(p3)

        p1 = figure(width=1000, height=500, toolbar_location="left")
        p1.xaxis.axis_label = "Epoch"
        p1.yaxis.axis_label = "Loss"
        r20 = p1.line(range(0, len(trainErrors['mape'])), trainErrors['mape'], color="red", line_width=1, line_alpha=0.8)
        r22 = p1.line(range(0, len(trainErrors['mape'])), valErrors['mape'], color="blue", line_width=1, line_alpha=0.8)
        r23 = p1.line(range(0, len(trainErrors['mape'])), testErrors['mape'], color="green", line_width=1,
                      line_alpha=0.8)
        legend2 = Legend(legends=[
            ("MAPE Training Set", [r20]),
            ("MAPE Validation Set", [r22]),
            ("MAPE Test Set", [r22])
        ], location=(40, 5))
        p1.add_layout(legend2, 'below')
        epochPlots.append(p1)


        return epochPlots

    def getTestSets(self, xInput, xOutput, percentage):
        fromT = 0
        last = xOutput.shape[0]
        toT = int(math.floor(last * (1 - percentage)))
        inputT = xInput[fromT:toT, :]
        outputT = xOutput[fromT:toT, :]
        inputV = xInput[toT + 1:last, :]
        outputV = xOutput[toT + 1:last, :]
        return inputT, outputT, inputV, outputV

    def calulateModelErrors(self, xInput, xOutput, scalerOutput, model):
        zoneIDs = range(1, 21)
        errorList = []
        errors = {}
        try:
            pV, outputV, predList, outputList = self.prepareCalculation(xInput, xOutput, scalerOutput, model)
            sumP = 0
            sumOutput = 0
            mapeList = []

            for zoneID in zoneIDs:
                errorList.append(np.mean((pV[zoneID] - outputV[zoneID]) ** 2))
                sumP += pV[zoneID]
                sumOutput += outputV[zoneID]

            errors["rmse"] = np.mean(errorList) ** 0.5
            sumP = sum(sumP.reshape(-1))
            sumOutput = sum(sumOutput.reshape(-1))
            errors["diff"] = (sumP - sumOutput) / sumOutput

            for i in range(len(predList)):
                if outputList[i] != 0:
                    mapeList.append(np.abs((predList[i] - outputList[i]) / outputList[i]))

            errors['mape'] = np.mean(mapeList)
        except ValueError:
            print "scaler out of bounds"
            pV = []
            outputV = []
            errors["rmse"] = numpy.nan
            errors["mape"] = numpy.nan
            errors["diff"] = numpy.nan
        return errors, pV, outputV

    def prepareCalculation(self, input, output, scaler, model):
        zoneIDs = range(1, 21)
        prediction = model.predict(input)
        pV = self.getSingleLoadPrediction(prediction, zoneIDs)
        outputV = self.getSingleLoadPrediction(output, zoneIDs)
        outputList = []
        predList = []
        for zoneID in zoneIDs:
            pV[zoneID] = scaler["zone_" + str(zoneID)].inverse_transform(pV[zoneID])
            outputV[zoneID] = scaler["zone_" + str(zoneID)].inverse_transform(outputV[zoneID])
            outputList.append(outputV[zoneID].reshape(-1))
            predList.append(pV[zoneID].reshape(-1))

        outputList = np.asarray(outputList).reshape(-1)
        predList = np.asarray(predList).reshape(-1)
        return pV, outputV, predList, outputList

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

    def getValidationInputOutput(self, stationIDs, timeWindow, scalerOutput, scalerInput, dfS, noFillZero = False, useHoliday = True, useWeekday = True, standardizationType="minmax"):
        backcastWeeks = ["2005-3-5", "2005-6-19", "2005-9-9", "2005-12-24",
                                 "2006-2-12", "2006-5-24", "2006-8-1", "2006-11-21","2008-6-30"]
        dfS = dfS.fillna(0)
        columns = range(1, timeWindow+1)
        zoneIDs = range(1,21)
        zoneColumns = ["zone_" + str(i) for i in zoneIDs]
        stationColumns = ["station_" + str(i) for i in stationIDs]
        dfNew = pd.DataFrame(columns=columns)

        holidayDict = energyload_class.getHolidayDict()

        for date in backcastWeeks:
            mask = (dfS['date'] == date)
            i = dfS.loc[mask].index[0]+24
            row = energyload_class.createInputOutputRow(dfS, i, columns, zoneColumns, stationColumns, 7*24, holidayDict, addSystemLevel = True, noFillZero=noFillZero, useHoliday=useHoliday, useWeekday=useWeekday)
            dfNew = dfNew.append([row],ignore_index=True)

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
            finalTestError = np.nan
            pV = []
            testOutput = []

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



#KerasModel(isShow= True, createHTML= True)
