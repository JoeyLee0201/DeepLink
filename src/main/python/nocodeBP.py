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

VECTOR_SIZE = 200
BATCH_SIZE = 100
STEPS = 5000
LEARNING_RATE = 0.1

docModel = Doc2Vec.load("test/nocodedoc50904245.model")


def cosine_similarity(vector1, vector2):
    dot_product = 0.0
    normA = 0.0
    normB = 0.0
    for a, b in zip(vector1, vector2):
        dot_product += a * b
        normA += a ** 2
        normB += b ** 2
    if normA == 0.0 or normB == 0.0:
        return 0
    else:
        return round(dot_product / ((normA**0.5)*(normB**0.5)) * 100, 2)


# text data
def text2vec(text, isHtml):
    if isHtml:
        words = preprocessor.processHTML(text)[1]
    else:
        words = preprocessor.preprocessToWord(text)
    return docModel.infer_vector(words)


def read_data(path='./train'):
    X = []
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
                X.append(cosine_similarity(commit, issue))
                Y.append(map['type'])

            file.close()
    return X, Y


# # shape=[batch_size, num-step]
# def make_batches(X, Y, batch_size, num_step):
#     num_batches = (len(X)-1) // (batch_size*num_step)
#     data = np.array(X[: batch_size*num_batches*num_step])
#     data = np.reshape(data, [batch_size, num_batches*num_step])
#     data_batches = np.split(data, num_batches, axis=1)
#
#     label = np.array(Y[: batch_size*num_batches*num_step])
#     label = np.reshape(label, [batch_size, num_batches*num_step])
#     label_batches = np.split(label, num_batches, axis=1)
#     return data_batches, label_batches


X, Y = read_data()

w1 = tf.Variable(tf.random_normal([1, 3], stddev=1, seed=1))
w2 = tf.Variable(tf.random_normal([3, 1], stddev=1, seed=1))

x = tf.placeholder(tf.float32, shape=(None, 1), name='x-input')
y_ = tf.placeholder(tf.float32, shape=(None, 1), name='y-input')

a = tf.matmul(x, w1)
y = tf.matmul(a, w2)

y = tf.sigmoid(y)
num_batches = len(X) // BATCH_SIZE

cross_entropy = -tf.reduce_mean(y_*tf.log(tf.clip_by_value(y, 1e-10, 1.0))
                                +(1-y)*tf.log(tf.clip_by_value(1-y, 1e-10, 1.0)))
train_step = tf.train.AdamOptimizer(0.001).minimize(cross_entropy)

with tf.Session() as sess:
    init_op = tf.global_variables_initializer()
    sess.run(init_op)
    for i in range(STEPS):
        start = (i*BATCH_SIZE) % len(X)
        end = min(start+BATCH_SIZE, len(X))
        sess.run(train_step, feed_dict={x: np.reshape(X[start: end], [end-start, 1]),
                                        y_: np.reshape(Y[start: end], [end-start, 1])})
