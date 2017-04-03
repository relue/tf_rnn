def objective(x):
    import modelKeras
    from hyperopt import STATUS_OK

    try:
        import dill as pickle
        print('Went with dill')
    except ImportError:
        import pickle


    modelOut = modelKeras.KerasModel(**x)
    data = {}
    data['loss'] = modelOut.results['loss'][-1]
    data['val_loss'] = modelOut.results['val_loss'][-1]
    data['test_loss'] = modelOut.results['test_loss'][-1]

    return {'loss': 1 ** 2, 'status': "ok" }
