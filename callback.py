import keras

class KaggleTest(keras.callbacks.Callback):
    testVals = []
    def __init__(self, KerasModel, input, output, scaler):
        self.input = input
        self.output = output
        self.scaler = scaler
        self.KerasModel = KerasModel

    def on_epoch_end(self, epoch, logs=None):
        finalTestError, pV, xOutputV = self.KerasModel.getTestError(self.model, self.input, self.output, self.scaler)
        self.testVals.append(finalTestError)

    def getHistory(self):
        return self.testVals
