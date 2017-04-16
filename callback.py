import keras

class EpochErrorRetrieve(keras.callbacks.Callback):
    testErrors = []
    trainErrors = {}
    valErrors = {}
    def __init__(self, KerasModel, inputTe, outputTe, inputT, outputT, inputV, outputV, scaler):
        self.inputTe = inputTe
        self.outputTe = outputTe
        self.inputT = inputT
        self.outputT = outputT
        self.inputV = inputV
        self.outputV = outputV
        self.scaler = scaler
        self.KerasModel = KerasModel
        self.trainErrors['rmse'] = []
        self.valErrors['rmse'] = []
        self.trainErrors['mape'] = []
        self.valErrors['mape'] = []

    def on_epoch_end(self, epoch, logs=None):
        finalTestError, pV, xOutputV = self.KerasModel.getTestError(self.model, self.inputTe, self.outputTe, self.scaler)
        errorsTrain, _, _ = self.KerasModel.calulateModelErrors(self.inputT, self.outputT, self.scaler, self.model)
        errorsVal, _, _ = self.KerasModel.calulateModelErrors(self.inputV, self.outputV, self.scaler, self.model)
        self.trainErrors['rmse'].append(errorsTrain['rmse'])
        self.valErrors['rmse'].append(errorsVal['rmse'])
        self.trainErrors['mape'].append(errorsTrain['mape'])
        self.valErrors['mape'].append(errorsVal['mape'])
        self.testErrors.append(finalTestError)

    def getErrors(self):
        return self.testErrors, self.trainErrors, self.valErrors
