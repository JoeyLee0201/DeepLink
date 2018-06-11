# -*- coding: UTF-8 -*-

import tensorflow as tf
import numpy as np

VECTOR_SIZE = 100
TRAIN_ITERS = 10000
BATCH_SIZE = 5
NUM_STEPS = 4
HIDDEN_SIZE = 100
N_CLASSES = 2
N_INPUTS = 100
LEARNING_RATE = 0.01


outputs1 = np.array([[[1.0, 1.0],[1.0, 1.0],[0.5, 1.0]],
            [[2.0, 2.0],[2.0, 2.0],[0.3, 0.2]],
            [[3.0, 3.0],[3.0, 3.0],[0.5, 0.4]]])
outputs2 = np.array([[[1.0, 1.0],[1.0, 1.0],[0.8, 0.9]],
            [[2.0, 2.0],[2.0, 2.0],[0.7, 0.9]],
            [[3.0, 3.0],[3.0, 3.0],[0.0, 0.0]]])

newoutput1 = outputs1[:, -1, :]
newoutput2 = outputs2[:, -1, :]
BATCH_SIZE = 3

target = [[0], [0], [0]]


def getScore(state1, state2):
    pooled_len_1 = tf.sqrt(tf.reduce_sum(state1 * state1, 1))
    pooled_len_2 = tf.sqrt(tf.reduce_sum(state2 * state2, 1))
    pooled_mul_12 = tf.reduce_sum(state1 * state2, 1)
    score = tf.div(pooled_mul_12, pooled_len_1 * pooled_len_2 + 1e-8, name="scores")  # +1e-8 avoid 'len_1/len_2 == 0'
    score = tf.reshape(score, [BATCH_SIZE, 1])
    return score

#  |t - cossimilar(state1, state2)|
def getLoss(score, t):
    # pooled_len_1 = tf.sqrt(tf.reduce_sum(state1 * state1, 1))
    # pooled_len_2 = tf.sqrt(tf.reduce_sum(state2 * state2, 1))
    # pooled_mul_12 = tf.reduce_sum(state1 * state2, 1)
    # score = tf.div(pooled_mul_12, pooled_len_1 * pooled_len_2+1e-8, name="scores")  #  +1e-8 avoid 'len_1/len_2 == 0'
    # score = tf.reshape(score, [BATCH_SIZE, 1])
    rs = t - score
    rs = tf.abs(rs)
    return tf.reduce_mean(rs)


# #  |t - cossimilar(state1, state2)|
# def getLoss(state1, state2, t):
#     pooled_len_1 = tf.sqrt(tf.reduce_sum(state1 * state1, 1))
#     pooled_len_2 = tf.sqrt(tf.reduce_sum(state2 * state2, 1))
#     pooled_mul_12 = tf.reduce_sum(state1 * state2, 1)
#     score = tf.div(pooled_mul_12, pooled_len_1 * pooled_len_2+1e-8, name="scores")
#     score = tf.reshape(score, [BATCH_SIZE, 1])
#     rs = t - score
#     return tf.abs(rs)


sess = tf.Session()
score = sess.run(getScore(newoutput1, newoutput2))
print score
print sess.run(getLoss(score, target))
#
#
# X1 = [[[1,1],[1,1]],
#       [[2,2],[2,2],[2,2]],
#       [[3,3]],
#       [[4,4],[4,4]],
#       [[5,5],[5,5]],
#       [[6,6],[6,6]],
#       [[7,7],[7,7]]]
# BATCH_SIZE = 2
# num_batches = len(X1) // BATCH_SIZE
# data1 = np.array(X1[: BATCH_SIZE*num_batches])
# data1 = np.reshape(data1, [BATCH_SIZE, num_batches])
# data_batches1 = np.split(data1, num_batches, axis=1)
# print data_batches1
# for d1 in data_batches1:
#     maxD = 0
#     for d in d1:
#         for dt in d:
#             maxD = max(maxD, len(list(dt)))
#             print dt
#     print maxD
#     for d in d1:
#         for dt in d:
#             todo = maxD - len(dt)
#             for index in range(todo):
#                 dt.append(np.zeros(2))
# print data_batches1
#
# Y= [2, 3, 1, 2, 2, 2, 2]
# num_batches = len(Y) // BATCH_SIZE
# label = np.array(Y[: BATCH_SIZE*num_batches])
# label = np.reshape(label, [BATCH_SIZE, num_batches])
# print label
# label_batches = np.split(label, num_batches, axis=1)
#
# label_batches = np.reshape(np.array(label_batches), [num_batches, BATCH_SIZE])
# print list(zip(data_batches1, label_batches))