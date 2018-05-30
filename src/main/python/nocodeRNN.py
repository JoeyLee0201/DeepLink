# -*- coding: UTF-8 -*-


from gensim.models import word2vec
from preprocessor import preprocessor

import tensorflow as tf
import numpy as np
import logging
import os
import json

logging.basicConfig(format='%(asctime)s : %(levelname)s : %(message)s', level=logging.INFO)

VECTOR_SIZE = 100
BATCH_SIZE = 2
NUM_STEPS = 4
STATE_SIZE = 10
LEARNING_RATE = 0.1

w2vModel = word2vec.Word2Vec.load('test/nocode50904245.model')


# text data
def text2vec(text, isHtml):
    if isHtml:
        words = preprocessor.processHTML(text)[1]
    else:
        words = preprocessor.preprocessToWord(text)
    res = []
    for word in words:
        try:
            res.append(w2vModel[word])
        except KeyError:
            res.append(np.zeros(VECTOR_SIZE))
    return res


def read_data(path='./train'):
    # commit_text = ''
    # issue_text = ''
    # commit_max = 0  # 667
    # issue_max = 0  # 413
    all_data = []
    filelist = os.listdir(path)
    for i in range(0, len(filelist)):
        filepath = os.path.join(path, filelist[i])
        if os.path.isfile(filepath):
            file = open(filepath, 'rb')
            testlist = json.loads(file.read())
            for map in testlist:
                commit = text2vec(map['commit'], False)
                issue = text2vec(map['issue'], True)
                all_data.append({'commit': commit,
                                 'issue': issue,
                                 'type': map['type']})
                # if commit_max < len(commit):
                #     commit_max = len(commit)
                #     commit_text = map['commit']
                # if issue_max < len(issue):
                #     issue_max = len(issue)
                #     issue_text = map['issue']
            file.close()
    return all_data  #, commit_max, issue_max, commit_text, issue_text
# d = read_data()
# print len(d[0])
# print d[1], d[3]
# print d[2], d[4]


# shape=[batch_size, num-step]
def make_batches(all_data, batch_size, num_step):
    num_batches = (len(all_data)-1) // (batch_size*num_step)
    data = np.array(all_data[: batch_size*num_batches*num_step])
    data = np.reshape(data, [batch_size, num_batches*num_step])
    data_batches = np.split(data, num_batches, axis=1)
    return data_batches


class Model(object):
    def __init__(self, is_training, batch_size, num_steps):
        self.batch_size = batch_size
        self. num_steps = num_steps



# def gen_batch(data, batch_size, num_steps):
#     data_length = len(data)
#
#     batch_partition_length = data_length // batch_size
#     data_x = np.zeros([batch_size, batch_partition_length, VECTOR_SIZE], dtype=np.float32)
#
#     for i in range(batch_size):
#         for j in range(batch_partition_length):
#             data_x[i][j] = data[i * batch_partition_length+j]
#     epoch_size = batch_partition_length // num_steps
#     for i in range(epoch_size):
#         x = data_x[:, i*num_steps:(i+1)*num_steps, :]
#         yield x
#
#
# def gen_epochs(n, data, batch_size, num_steps):
#     for i in range(n):
#         yield gen_batch(data, batch_size, num_steps)

#
# x = tf.placeholder(tf.float32, [BATCH_SIZE, NUM_STEPS, VECTOR_SIZE])
#
# init_state = tf.zeros([BATCH_SIZE, STATE_SIZE, VECTOR_SIZE])
#
# rnn_inputs = tf.unstack(x, axis=1)
# with tf.variable_scope('rnn_cell'):
#     W = tf.get_variable('W', [STATE_SIZE + VECTOR_SIZE, STATE_SIZE])
#     b = tf.get_variable('b', [STATE_SIZE], initializer=tf.constant_initializer(0.0))
#
#
# def rnn_cell(rnn_input, state):
#     with tf.variable_scope('rnn_cell', reuse=True):
#         W = tf.get_variable('W', [STATE_SIZE + VECTOR_SIZE, STATE_SIZE])
#         b = tf.get_variable('b', [STATE_SIZE], initializer=tf.constant_initializer(0.0))
#     return tf.tanh(tf.matmul(tf.concat((rnn_input, state), 1), W)+b)
#
#
# state = init_state
# rnn_outputs = []
# for rnn_input in rnn_inputs:
#     state = rnn_cell(rnn_input, state)
#     rnn_outputs.append(state)
# final_state = rnn_outputs[-1]
#
# with tf.variable_scope('softmax'):
#     W = tf.get_variable('W', [STATE_SIZE, n_classes])
#     b = tf.get_variable('b', [n_classes])
# logits = [tf.matmul(rnn_output, W)+b for rnn_output in rnn_outputs]
# predictions = [tf.nn.softmax(logit) for logit in logits]
# # Turn our y placeholder into a list of labels
# y_as_lists = tf.unstack(y, num=NUM_STEPS, axis=1)
#
# #losses and train_step
# losses = [tf.nn.sparse_softmax_cross_entropy_with_logits(labels=label, logits=logit) for label, logit in zip(y_as_lists, predictions)]
# total_loss = tf.reduce_mean(losses)
# train_step = tf.train.GradientDescentOptimizer(LEARNING_RATE).minimize(total_loss)
#
#
# def train_network(num_epochs, num_steps, state_size):
#     with tf.Session() as sess:
#         sess.run(tf.global_variables_initializer())
#         for idx, epoch in enumerate(gen_epochs(num_epochs, num_steps)):
#             training_state = np.zeros((BATCH_SIZE, state_size))
#             for step, (X, Y) in enumerate(epoch):
#                 tr_losses, training_loss_, training_state, _ = \
#                     sess.run([losses,
#                               total_loss,
#                               final_state,
#                               train_step],
#                              feed_dict={x: X, init_state: training_state})
#
#
# training_losses = train_network(1, NUM_STEPS, STATE_SIZE)
