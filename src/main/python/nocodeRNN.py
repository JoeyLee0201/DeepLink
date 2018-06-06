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
BATCH_SIZE = 20
# NUM_STEPS = 4
HIDDEN_SIZE = 100
# N_CLASSES = 2
N_INPUTS = 100
LEARNING_RATE = 0.01

tf.get_default_graph()
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
            res.append(np.zeros(VECTOR_SIZE))
    return res


#  shape = [None, seq len, Vec size]
def read_data(path='./train'):
    # commit_text = ''
    # issue_text = ''
    # commit_max = 0  # 667
    # issue_max = 0  # 413
    X1 = []
    X2 = []
    L1 = []
    L2 = []
    Y = []
    filelist = os.listdir(path)
    for i in range(0, 1):
        filepath = os.path.join(path, filelist[i])
        if os.path.isfile(filepath):
            file = open(filepath, 'rb')
            testlist = json.loads(file.read())
            for map in testlist:
                commit = text2vec(map['commit'], False)
                issue = text2vec(map['issue'], True)
                L1.append(len(commit))
                X1.append(commit)
                L2.append(len(issue))
                X2.append(issue)
                Y.append(float(map['type']))
            file.close()
    return X1, X2, L1, L2, Y


# shape=[batch_size, None]
def make_batches(data, batch_size):
    X1, X2, L1, L2, Y = data
    num_batches = len(Y) // batch_size
    data1 = np.array(X1[: batch_size*num_batches])
    data1 = np.reshape(data1, [batch_size, num_batches])
    data_batches1 = np.split(data1, num_batches, axis=1)  #  list
    data_batches1_rs = []
    for d1 in data_batches1:
        sub_batch = []
        maxD = 0
        for d in d1:
            for dt in d:
                maxD = max(maxD, len(dt))
        for d in d1:
            for dt in d:
                todo = maxD - len(dt)
                for index in range(todo):
                    dt.append(np.zeros(VECTOR_SIZE))
                sub_batch.append(np.array(dt))
        data_batches1_rs.append(np.array(sub_batch))

    data2 = np.array(X2[: batch_size*num_batches])
    data2 = np.reshape(data2, [batch_size, num_batches])
    data_batches2 = np.split(data2, num_batches, axis=1)
    data_batches2_rs = []
    for d2 in data_batches2:
        sub_batch = []
        maxD = 0
        for d in d2:
            for dt in d:
                maxD = max(maxD, len(dt))
        for d in d2:
            for dt in d:
                todo = maxD - len(dt)
                for index in range(todo):
                    dt.append(np.zeros(VECTOR_SIZE))
                sub_batch.append(np.array(dt))
        data_batches2_rs.append(np.array(sub_batch))

    len1 = np.array(L1[: batch_size*num_batches])
    len1 = np.reshape(len1, [batch_size, num_batches])
    len_batches1 = np.split(len1, num_batches, axis=1)
    len_batches1 = np.reshape(np.array(len_batches1), [num_batches, BATCH_SIZE])

    len2 = np.array(L2[: batch_size * num_batches])
    len2 = np.reshape(len2, [batch_size, num_batches])
    len_batches2 = np.split(len2, num_batches, axis=1)
    len_batches2 = np.reshape(np.array(len_batches2), [num_batches, BATCH_SIZE])

    label = np.array(Y[: batch_size*num_batches])
    label = np.reshape(label, [batch_size, num_batches])
    label_batches = np.split(label, num_batches, axis=1)
    return list(zip(data_batches1_rs, data_batches2_rs, len_batches1, len_batches2, label_batches))


input1 = tf.placeholder(tf.float32, [BATCH_SIZE, None, VECTOR_SIZE])
input2 = tf.placeholder(tf.float32, [BATCH_SIZE, None, VECTOR_SIZE])
len1 = tf.placeholder(tf.int32, [BATCH_SIZE, ])
len2 = tf.placeholder(tf.int32, [BATCH_SIZE, ])
target = tf.placeholder(tf.float32, [BATCH_SIZE, 1])


def RNN(input_data, seq_len):
    rnn_cell = tf.nn.rnn_cell.BasicLSTMCell(HIDDEN_SIZE)
    rnn_cell = tf.nn.rnn_cell.MultiRNNCell([rnn_cell for _ in range(3)])
    initial_state = rnn_cell.zero_state(BATCH_SIZE, dtype=tf.float32)
    outputs, state = tf.nn.dynamic_rnn(rnn_cell, input_data, sequence_length=seq_len, initial_state=initial_state, dtype=tf.float32)
    return outputs, state


with tf.variable_scope("commit"):
    outputs1, _ = RNN(input1, len1)
with tf.variable_scope("issue"):
    outputs2, _ = RNN(input2, len2)

newoutput1 = outputs1[:, -1, :]
newoutput2 = outputs2[:, -1, :]


#  |t - cossimilar(state1, state2)|
def getLoss(state1, state2, t):
    pooled_len_1 = tf.sqrt(tf.reduce_sum(state1 * state1, 1))
    pooled_len_2 = tf.sqrt(tf.reduce_sum(state2 * state2, 1))
    pooled_mul_12 = tf.reduce_sum(state1 * state2, 1)
    score = tf.div(pooled_mul_12, pooled_len_1 * pooled_len_2, name="scores")
    score = tf.reshape(score, [BATCH_SIZE, 1])
    rs = t - score
    return tf.abs(rs)


# Define loss and optimizer
loss_op = getLoss(newoutput1, newoutput2, target)

optimizer = tf.train.GradientDescentOptimizer(learning_rate=LEARNING_RATE)
train_op = optimizer.minimize(loss_op)

# Initialize the variables (i.e. assign their default value)
init = tf.global_variables_initializer()
train_batches = make_batches(read_data(), BATCH_SIZE)
# Start training
with tf.Session() as sess:
    sess.run(init)

    for step in range(TRAIN_ITERS):
        print step, '>>>>>>>>>>>>>>>>'
        for x1, x2, l1, l2, y in train_batches:
            # print len(x1), '-------'
            # print x1.shape
            # for t1 in x1:
            #     print t1.shape
            #     break
            #     for d in t1:
            #         print len(d)
            #         for w in d:
            #             if len(w)==VECTOR_SIZE:
            #                 pass
            #             else:
            #                 print '=', len(w)
            # print len(x2), '-------'
            # print x2.shape
            # for t2 in x2:
            #     print t2.shape
            #     break
            #     for d in t2:
            #         print len(d)
            #         for w in d:
            #             if len(w)==VECTOR_SIZE:
            #                 pass
            #             else:
            #                 print '=', len(w)
            # print l1.shape
            # print l2.shape
            # print y.shape
            sess.run(train_op, feed_dict={input1: x1, input2: x2, len1: l1, len2: l2, target: y})
            if step % 100 == 0 or step == 1:
                loss = sess.run([loss_op], feed_dict={input1: x1, input2: x2, len1: l1, len2: l2, target: y})
                print("Step " + str(step) + ", Minibatch Loss= " + "{:.4f}".format(loss))

    print("Optimization Finished!")