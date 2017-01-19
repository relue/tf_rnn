
'''Todos
- Regression als Vergleich
- Anzeige kapseln unabhaengig von Merkmalszahl
- Netze speichern
- Logarithmieren kapseln
- Debugging etablieren evtl Tensor Graph Flow
- RNN mit BPOT implementieren
'''
import tensorflow as tf
import matplotlib.pyplot as plt
import ts_gen
import math
import numpy

rows = 10000
isTransform = True
timeWindow = 1
dimensionsX = 2
testIndex = rows/2
ar = ts_gen.generate_ts(rows, isTransform)
dataX = ar[0:testIndex, 0:2]
dataY = ar[0:testIndex, 2]
testDataX = ar[testIndex-1:rows-1, 0:2]
testDataY = ar[testIndex-1:rows-1, 2]

#dataX = ts_gen.createInput(dataX, timeWindow, dimensionsX)
#testDataX = ts_gen.createInput(testDataX, timeWindow, dimensionsX)
#input_vector_size = dimensionsX * (timeWindow+1)
input_vector_size = 2
n_nodes = 10
n_classes = 1
batches = 10
hm_epochs = 70
hiddenLayerCount = 2

x = tf.placeholder('float', [None, input_vector_size])
y = tf.placeholder('float')

def neural_network_model(data):
    data = tf.cast(data, tf.float32)
    hidden_1_layer = {'weights':tf.Variable(tf.random_normal([input_vector_size, n_nodes])),
                          'biases':tf.Variable(tf.random_normal([n_nodes]))}
    l1 = tf.add(tf.matmul(data,hidden_1_layer['weights']), hidden_1_layer['biases'])
    l1 = tf.nn.relu(l1)
    layerPrev = l1

    for lc in range(2, hiddenLayerCount+1):
        hidden_layer_x = {'weights':tf.Variable(tf.random_normal([n_nodes, n_nodes])),
                          'biases':tf.Variable(tf.random_normal([n_nodes]))}

        layerX = tf.add(tf.matmul(layerPrev,hidden_layer_x['weights']), hidden_layer_x['biases'])
        layerX = tf.nn.relu(layerX)
        layerPrev = layerX

    output_layer = {'weights':tf.Variable(tf.random_normal([n_nodes, n_classes])),
                    'biases':tf.Variable(tf.random_normal([n_classes])),}

    output = tf.matmul(layerPrev,output_layer['weights']) + output_layer['biases']

    return output

def train_neural_network(dataX, dataY):
    prediction = neural_network_model(x)
    error = (prediction - y) ** 2
    cost = tf.reduce_mean( error )

    error2 = (tf.exp(prediction) - tf.exp(y)) ** 2
    cost2 = tf.reduce_mean( error2 )

    optimizer = tf.train.AdamOptimizer().minimize(cost)

    with tf.Session() as sess:
        sess.run(tf.initialize_all_variables())

        for epoch in range(hm_epochs):
            epoch_loss = 0
            for batch_i in range(1, batches+1):
                batchDataX = ts_gen.getBatch(dataX, batch_i, batches)
                batchDataY = ts_gen.getBatch(dataY, batch_i, batches)
                sess.run(optimizer,feed_dict={x: batchDataX, y: batchDataY})
            c = sess.run(cost, feed_dict={x: dataX, y: dataY})
            print('Epoch', epoch, 'completed out of',hm_epochs,'loss:',c)

        p = sess.run(prediction, feed_dict={x: testDataX, y: testDataY})
        t = sess.run(cost, feed_dict={x: testDataX, y: testDataY})
        c = sess.run(cost2, feed_dict={x: testDataX, y: testDataY})

        print('Test:',numpy.exp(t))
        print('TestScaled:',c)
    return p

scaledX = numpy.exp(testDataX)
scaledY = numpy.exp(testDataY)
predictionReal = train_neural_network(dataX,dataY)
error3 = (numpy.exp(predictionReal) - numpy.exp(testDataY)) ** 2
cost3 = numpy.mean(error3)
print('TestScaled:',cost3)

plt.plot(range(0,testIndex),scaledY)
plt.plot(range(0,testIndex), scaledX[:,0])
#plt.plot(range(0,testIndex),dataX[:,input_vector_size-2])
#plt.plot(range(0,testIndex),dataX[:,input_vector_size-1])
plt.plot(range(0,testIndex),numpy.exp(predictionReal))
plt.legend(['y(t)', 'x1(t)', 'p(t)'], loc='upper left')
plt.show()
