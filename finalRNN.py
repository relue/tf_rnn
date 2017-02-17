from __future__ import print_function

import tensorflow as tf
import random
import pandas as pd
import numpy as np

import energyload_class

pd.set_option('display.height', 1000)
pd.set_option('display.max_rows', 100)
pd.set_option('display.max_columns', 19)
pd.set_option('display.width', 1000)

# ==========
#   MODEL
# ==========

# Parameters
learning_rate = 0.01
training_iters = 1000000
batch_size = 128
display_step = 10
hm_epochs = 10

# Network Parameters
timeWindow = 24
n_hidden = 2 # hidden layer num of features
n_classes = 1 # linear sequence or not

x = tf.placeholder("float", [None, timeWindow, 1])
y = tf.placeholder("float", [None, 1])

df, dfHourly = energyload_class.init_dfs()
batchSize = 1000

def createX(df, batchSize):
    station_id = "station_1"
    zone_id = "zone_1"
    timeWindow = 7
    columns = range(timeWindow, -1, -1)
    dfNew = pd.DataFrame(columns=columns)

    n = 0
    for i in range(0, batchSize):
        if i >= timeWindow:
            columnList = []
            for t in columns:
                columnList.append([df.iloc[i-t][station_id], df.iloc[i-t][zone_id]])

            row=pd.Series(columnList,columns)
            dfNew = dfNew.append([row],ignore_index=True)
            n += 1

    tfInput = []
    tfOutput= []
    for t in columns:
        if t == 0:
            tfOutput.append(dfNew[t].tolist())
        else:
            tfInput.append(dfNew[t].tolist())

    return tfInput, tfOutput

xInput, xOutput = createX(dfHourly, batchSize)

# Define weights
weights = {
    'out': tf.Variable(tf.random_normal([n_hidden, n_classes]))
}
biases = {
    'out': tf.Variable(tf.random_normal([n_classes]))
}

def dynamicRNN(x, weights, biases):
    lstm_cell = tf.nn.rnn_cell.BasicRNNCell(n_hidden)
    outputs, states = tf.nn.rnn(lstm_cell, x, dtype=tf.float32)
    return tf.matmul(outputs, weights['out']) + biases['out']

prediction = dynamicRNN(x, weights, biases)
error = (prediction - y) ** 2
cost = tf.reduce_mean( error )

optimizer = tf.train.AdamOptimizer().minimize(cost)

# Define loss and optimizer

#optimizer = tf.train.GradientDescentOptimizer(learning_rate=learning_rate).minimize(cost)

# Initializing the variables
init = tf.global_variables_initializer()

# Launch the graph
with tf.Session() as sess:
    sess.run(init)
    for epoch in range(hm_epochs):
        sess.run(optimizer, feed_dict={x: xInput, y: xOutput})
        p = sess.run(prediction, feed_dict={x: xInput, y: xOutput})
