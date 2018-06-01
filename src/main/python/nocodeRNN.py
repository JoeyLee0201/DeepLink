# -*- coding: UTF-8 -*-


from gensim.models import word2vec
from preprocessor import preprocessor
from gensim.models.doc2vec import Doc2Vec

import tensorflow as tf
import numpy as np
import logging
import os
import json

logging.basicConfig(format='%(asctime)s : %(levelname)s : %(message)s', level=logging.INFO)

VECTOR_SIZE = 100
TRAIN_ITERS = 10000
BATCH_SIZE = 5
NUM_STEPS = 4
HIDDEN_SIZE = 100
N_CLASSES = 2
N_INPUTS = 100
LEARNING_RATE = 0.01

wordModel = word2vec.Word2Vec.load('test/nocode50904245.model')


# text data
def text2vec(text, isHtml):
    if isHtml:
        words = preprocessor.processHTML(text)[1]
    else:
        words = preprocessor.preprocessToWord(text)
    res = []
    for word in words:
        try:
            res.append(wordModel[word])
        except KeyError:
            res.append(tf.zeros(VECTOR_SIZE))
    return res

#  shape = [None, seq len, Vec size]
def read_data(path='./train'):
    # commit_text = ''
    # issue_text = ''
    # commit_max = 0  # 667
    # issue_max = 0  # 413
    X1 = []
    X2 = []
    Y = []
    filelist = os.listdir(path)
    for i in range(0, len(filelist)):
        filepath = os.path.join(path, filelist[i])
        if os.path.isfile(filepath):
            file = open(filepath, 'rb')
            testlist = json.loads(file.read())
            for map in testlist:
                commit = text2vec(map['commit'], False)
                issue = text2vec(map['issue'], True)
                X1.append(commit)
                X2.append(issue)
                Y.append(map['type'])
            file.close()
    return X1, X2, Y


# shape=[batch_size, None]
def make_batches(data, batch_size):
    X1, X2, Y = data
    num_batches = len(X1) // batch_size
    data1 = np.array(X1[: batch_size*num_batches])
    data1 = np.reshape(data1, [batch_size, num_batches])
    data_batches1 = np.split(data1, num_batches, axis=1)

    data2 = np.array(X2[: batch_size*num_batches])
    data2 = np.reshape(data2, [batch_size, num_batches])
    data_batches2 = np.split(data2, num_batches, axis=1)

    label = np.array(Y[: batch_size*num_batches])
    label = np.reshape(label, [batch_size, num_batches])
    label_batches = np.split(label, num_batches, axis=1)
    return list(zip(data_batches1, data_batches2, label_batches))


input1 = tf.placeholder(tf.int32, [BATCH_SIZE, None, VECTOR_SIZE])
input2 = tf.placeholder(tf.int32, [BATCH_SIZE, None, VECTOR_SIZE])
target = tf.placeholder(tf.int32, [BATCH_SIZE, N_CLASSES])


def word2Vector(index):
    return wordModel[wordModel.wv.index2word[index]]


def RNN(input_data):
    rnn_cell = tf.nn.rnn_cell.BasicRNNCell(HIDDEN_SIZE)
    initial_state = rnn_cell.zero_state(BATCH_SIZE, dtype=tf.float32)
    outputs, state = tf.nn.dynamic_rnn(rnn_cell, input_data,
                                               initial_state=initial_state,
                                               dtype=tf.float32)
    return outputs, state


outputs1, state1 = RNN(input1)
outputs2, state2 = RNN(input2)

logits = tf.tanh( tf.matmul ( x, w ) + b)
prediction = tf.nn.softmax(logits)

# Define loss and optimizer
loss_op = tf.reduce_mean(tf.nn.softmax_cross_entropy_with_logits(
        logits=logits, labels=target))


optimizer = tf.train.GradientDescentOptimizer(learning_rate=LEARNING_RATE)
train_op = optimizer.minimize(loss_op)
correct_pred = tf.equal(tf.argmax(prediction, 1), tf.argmax(target, 1))
accuracy = tf.reduce_mean(tf.cast(correct_pred, tf.float32))

# Initialize the variables (i.e. assign their default value)
init = tf.global_variables_initializer()
train_batches = make_batches(read_data(), BATCH_SIZE)
# Start training
with tf.Session() as sess:
    sess.run(init)

    for step in range(TRAIN_ITERS):
        for x1, x2, y in train_batches:
            sess.run(train_op, feed_dict={input1: x1, input2: x2, target: y})
            if step % 100 == 0 or step == 1:
                loss, acc = sess.run([loss_op, accuracy], feed_dict={input1: x1, input2: x2, target: y})
                print("Step " + str(step) + ", Minibatch Loss= " + \
                      "{:.4f}".format(loss) + ", Training Accuracy= " + \
                      "{:.3f}".format(acc))

    print("Optimization Finished!")


# x = tf.placeholder(tf.float32, [None, NUM_STEPS, N_INPUTS])
# y = tf.placeholder(tf.float32, [None, N_CLASSES])
#
# weights = {
#     'out': tf.Variable(tf.random_normal([num_hidden, num_classes]))
# }
# biases = {
#     'out': tf.Variable(tf.random_normal([num_classes]))
# }
#
#
# def RNN(x, weights, biases):
#     x = tf.unstack(x, timesteps, 1)
#     lstm_cell = rnn.BasicLSTMCell(num_hidden, forget_bias=1.0)
#     outputs, states = rnn.static_rnn(lstm_cell, x, dtype=tf.float32)
#     return tf.matmul(outputs[-1], weights['out']) + biases['out']
#
#
# logits = RNN(x, weights, biases)
# prediction = tf.nn.softmax(logits)
#
# # Define loss and optimizer
# loss_op = tf.reduce_mean(tf.nn.softmax_cross_entropy_with_logits(
#     logits=logits, labels=Y))
# optimizer = tf.train.GradientDescentOptimizer(learning_rate=learning_rate)
# train_op = optimizer.minimize(loss_op)
#
# # Evaluate model (with test logits, for dropout to be disabled)
# correct_pred = tf.equal(tf.argmax(prediction, 1), tf.argmax(Y, 1))
# accuracy = tf.reduce_mean(tf.cast(correct_pred, tf.float32))
#
# # Initialize the variables (i.e. assign their default value)
# init = tf.global_variables_initializer()
#
# # Start training
# with tf.Session() as sess:
#
#     # Run the initializer
#     sess.run(init)
#
#     for step in range(1, training_steps+1):
#         batch_x, batch_y = mnist.train.next_batch(batch_size)
#         # Reshape data to get 28 seq of 28 elements
#         batch_x = batch_x.reshape((batch_size, timesteps, num_input))
#         # Run optimization op (backprop)
#         sess.run(train_op, feed_dict={X: batch_x, Y: batch_y})
#         if step % display_step == 0 or step == 1:
#             # Calculate batch loss and accuracy
#             loss, acc = sess.run([loss_op, accuracy], feed_dict={X: batch_x,
#                                                                  Y: batch_y})
#             print("Step " + str(step) + ", Minibatch Loss= " + \
#                   "{:.4f}".format(loss) + ", Training Accuracy= " + \
#                   "{:.3f}".format(acc))
#
#     print("Optimization Finished!")
#
#     # Calculate accuracy for 128 mnist test images
#     test_len = 128
#     test_data = mnist.test.images[:test_len].reshape((-1, timesteps, num_input))
#     test_label = mnist.test.labels[:test_len]
#     print("Testing Accuracy:", \
#         sess.run(accuracy, feed_dict={X: test_data, Y: test_label}))
