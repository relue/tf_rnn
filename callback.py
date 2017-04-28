import keras

class EpochErrorRetrieve(keras.callbacks.Callback):
    testErrors = {}
    trainErrors = {}
    valErrors = {}
    def __init__(self, KerasModel, inputTe, outputTe, inputT, outputT, inputV, outputV, inputV2,outputV2, scaler):
        self.inputTe = inputTe
        self.outputTe = outputTe
        self.inputT = inputT
        self.outputT = outputT
        self.inputV = inputV
        self.outputV = outputV
        self.inputV2 = inputV2
        self.outputV2 = outputV2
        self.scaler = scaler
        self.KerasModel = KerasModel
        self.trainErrors['rmse'] = []
        self.valErrors['rmse'] = []
        self.testErrors['rmse'] = []

        self.trainErrors['mape'] = []
        self.valErrors['mape'] = []
        self.testErrors['mape'] = []


    def on_epoch_end(self, epoch, logs=None):
        #finalTestError, pV, xOutputV = self.KerasModel.getTestError(self.model, self.inputTe, self.outputTe, self.scaler)
        errorsTrain, _, _ = self.KerasModel.calulateModelErrors(self.inputT, self.outputT, self.scaler, self.model)
        errorsVal, _, _ = self.KerasModel.calulateModelErrors(self.inputV, self.outputV, self.scaler, self.model)
        errorsTest, _, _ = self.KerasModel.calulateModelErrors(self.inputV2, self.outputV2, self.scaler, self.model)
        self.trainErrors['rmse'].append(errorsTrain['rmse'])
        self.valErrors['rmse'].append(errorsVal['rmse'])
        self.testErrors['rmse'].append(errorsTest['rmse'])
        self.trainErrors['mape'].append(errorsTrain['mape'])
        self.valErrors['mape'].append(errorsVal['mape'])
        self.testErrors['mape'].append(errorsTest['mape'])
        #self.testErrors.append(finalTestError)

    def getErrors(self):
        return self.testErrors, self.trainErrors, self.valErrors
