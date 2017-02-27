from __future__ import print_function

import tensorflow as tf
import random
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import energyload_class
from time import *
import os
import math

pd.set_option('display.height', 1000)
pd.set_option('display.max_rows', 100)
pd.set_option('display.max_columns', 19)
pd.set_option('display.width', 1000)


# ==========
#   MODEL
# ==========
t1 = clock()
newInput = False # reinit Feature Vektor if true (set this when windowSize ist updated)

# Parameters
learning_rate = 0.01
hm_epochs = 20
n_hidden = 10 # hidden layer num of features
n_classes = 1 # linear sequence or not
batchSize = 100
timeWindow = 1
inputSize = 3

jumpSequences = False
isLogarithmic = False
isMLP = True

if newInput:
    df = energyload_class.init_dfs(False, False)
    df['date'] = pd.to_datetime(df['date'])
    df['weekday'] = df['date'].dt.dayofweek

def getBatch(gInput, gOutput, i):
    fromI = i*batchSize
    toI = fromI + batchSize
    if isMLP:
        inputR = gInput[fromI:toI,:]
    else:
        inputR = gInput[:,fromI:toI]
    return inputR, gOutput[fromI:toI]

def createX(save = False, isMLP = False):
    columns = range(timeWindow, -1, -1)
    if save:
        station_id = "station_1"
        zone_id = "zone_1"

        dfNew = pd.DataFrame(columns=columns)
        for i in range(0, 10000, timeWindow if jumpSequences else 1):#len(df.index)
            if i >= timeWindow:
                columnList = []
                for t in columns:
                    #columnList.append([df.iloc[i-t][station_id], df.iloc[i-t][zone_id]])
                    columnList.append([df.iloc[i-t]['hour'], df.iloc[i-t]['weekday'], df.iloc[i-t][station_id], df.iloc[i-t][zone_id], ])
                row=pd.Series(columnList,columns)
                dfNew = dfNew.append([row],ignore_index=True)
        dfNew[['hour','weekday','temp','load']] = dfNew[0].apply(pd.Series)
        #dfNew[['load']] = dfNew[0].apply(pd.Series)
        dfNew.to_pickle("rnnInput.pd")
    else:
        dfNew = pd.read_pickle('rnnInput.pd')

    tfInput = []
    tfOutput= []
    for t in columns:
        if t == 0:
            tfOutput = np.asarray(dfNew['load'].tolist())
        else:
            tfInput.append(dfNew[t].tolist())

    if isMLP:
        tfInput = dfNew.loc[:,['hour','weekday','temp']]

    if isLogarithmic:
        return np.log(np.asarray(tfInput)),np.log(tfOutput)
    else:
        return np.asarray(tfInput),tfOutput

def dynamicRNN(x, weights, biases):
    #for i in tf.split(x, timeWindow, 0):
    #   inputs.append(tf.reshape(i, (batchSize, inputSize)))
    x = tf.cast(x, tf.float32)
    with tf.name_scope('summaries'):
        inputs = tf.unpack(x, timeWindow, 0)

        lstm_cell = tf.nn.rnn_cell.BasicRNNCell(n_hidden)
        outputs, states = tf.nn.rnn(lstm_cell, inputs, dtype=tf.float32) #inputs[::-1] #reverse Window
        #tf.summary.histogram('hidden outputs', outputs)

        outputs = tf.pack(outputs)
        outputs = tf.transpose(outputs, [1, 0, 2])

        # Hack to build the indexing and retrieve the right output.
        batch_size = tf.shape(outputs)[0]
        # Start indices for each sample
        index = tf.range(0, batch_size) * timeWindow + (timeWindow - 1)
        # Indexing
        outputs = tf.gather(tf.reshape(outputs, [-1, n_hidden]), index)
        with tf.name_scope('train'):
            with tf.name_scope('weights'):
             #   tf.summary.histogram('weights', weights['out'])

                tf.summary.tensor_summary('weights', weights['out'])
            tf.summary.tensor_summary('biases', biases['out'])
    return tf.matmul(outputs, weights['out'])  + biases['out']

hiddenLayerCount = 6

def neural_network_model(data):
    data = tf.cast(data, tf.float32)
    hidden_1_layer = {'weightsM':tf.Variable(tf.random_normal([inputSize, n_hidden])),
                          'biasesM':tf.Variable(tf.random_normal([n_hidden]))}
    l1 = tf.add(tf.matmul(data,hidden_1_layer['weightsM']), hidden_1_layer['biasesM'])
    l1 = tf.nn.relu(l1)
    layerPrev = l1

    for lc in range(2, hiddenLayerCount+1):
        hidden_layer_x = {'weightsM':tf.Variable(tf.random_normal([n_hidden, n_hidden])),
                          'biasesM':tf.Variable(tf.random_normal([n_hidden]))}

        layerX = tf.add(tf.matmul(layerPrev,hidden_layer_x['weightsM']), hidden_layer_x['biasesM'])
        layerX = tf.nn.relu(layerX)
        layerPrev = layerX

    output_layer = {'weightsM':tf.Variable(tf.random_normal([n_hidden, n_classes])),
                    'biasesM':tf.Variable(tf.random_normal([n_classes])),}

    output = tf.matmul(layerPrev,output_layer['weightsM']) + output_layer['biasesM']

    return output

def debug(x):

    x = tf.cast(x, tf.float32)
    inputs2 = tf.unpack(x, timeWindow, 0)

    lstm_cell2 = tf.nn.rnn_cell.BasicRNNCell(n_hidden)
    outputs2, states2 = tf.nn.rnn(lstm_cell2, inputs2, dtype=tf.float32, scope = "new")
    outputs3 = tf.pack(outputs2)
    outputs3 = tf.transpose(outputs3, [1, 0, 2])

    batch_size = tf.shape(outputs3)[0]
    index = tf.range(0, batch_size) * timeWindow + (timeWindow - 1)
    outputs3 = tf.gather(tf.reshape(outputs3, [-1, n_hidden]), index)

    return inputs2, x, outputs2, states2, outputs3

xInput, xOutput = createX(newInput, isMLP = True)

#xInput, xOutput = createX(newInput)
#x = tf.placeholder("float", [timeWindow, None, inputSize])
x = tf.placeholder('float', [None, inputSize])
y = tf.placeholder("float", [None])

# Define weights
weights = {
    'out': tf.Variable(tf.random_normal([n_hidden, n_classes]))
}
biases = {
    'out': tf.Variable(tf.random_normal([n_classes]))
}

prediction = neural_network_model(x)
#prediction = dynamicRNN(x, weights, biases)

error = (prediction - y) ** 2
cost = tf.reduce_mean(error)
tf.summary.scalar('cost', cost)
optimizer = tf.train.AdamOptimizer().minimize(cost)
#optimizer = tf.train.GradientDescentOptimizer(learning_rate=learning_rate).minimize(cost)

#dB = debug(x)

# Initializing the variables
init = tf.global_variables_initializer()

merged = tf.summary.merge_all()


# Launch the graph
with tf.Session() as sess:
    train_writer = tf.summary.FileWriter(os.getcwd() + '/train',
                                      sess.graph)
    sess.run(init)
    batches = (len(xOutput) // batchSize)
    learnStep = 1
    for epoch in range(hm_epochs):
        for batchI in range(0,batches+1):
            xInputBatch, xOutputBatch = getBatch(xInput, xOutput, batchI)
            _, c, summary = sess.run([optimizer, cost, merged], feed_dict={x: xInputBatch, y: xOutputBatch})
            #w, b = sess.run([weights, biases], feed_dict={x: xInputBatch, y: xOutputBatch})
            #print("w", w, "b", b)
            print('cost:',c," epoch",epoch," batch",batchI)
            learnStep += 1
            train_writer.add_summary(summary, learnStep)
            p = sess.run(prediction, feed_dict={x: xInput, y: xOutput})

            #print(p)
            #inps1,inps2, d, st, d3 = sess.run(dB, feed_dict={x: xInputBatch, y: xOutputBatch})
            #print(d,'d3',d3)
            #print('ins', inps1, 'ins2', inps2)
            #raise Exception()

    err = sess.run(prediction, feed_dict={x: xInput, y: xOutput})
    print('errorC:',err)
    errorC = sess.run(cost, feed_dict={x: xInput, y: xOutput})
    print('errorC:',errorC)

    plt.plot(range(0,len(xOutput)),p)
    plt.plot(range(0,len(xOutput)), xOutput)
    plt.legend(['p(t)', 'y(t)'], loc='upper left')
    plt.show()
