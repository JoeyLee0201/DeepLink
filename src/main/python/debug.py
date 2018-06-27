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
TRAIN_ITERS = 300
BATCH_SIZE = 16
HIDDEN_SIZE = 100
N_INPUTS = 100
LEARNING_RATE = 0.01

LSTM_KEEP_PROB = 0.9

# REPO_ID = 12499251
REPO_ID = 20587599
MAX_RECORD = {'step': -1, 'acc': 0.0}

wordModel = word2vec.Word2Vec.load('test/nocode%d.model' % REPO_ID)


# text data
def text2vec(text, isHtml):
    if isHtml:
        seqs = preprocessor.processHTMLNoCamel(text)
    else:
        seqs = preprocessor.preprocessNoCamel(text)
    res = []
    for seq in seqs:
        for word in seq:
            try:
                res.append(wordModel[word])
            except KeyError:
                res.append(np.zeros(VECTOR_SIZE))
    return res


#  shape = [None, seq len, Vec size]
def read_data(path):
    X1 = []
    X2 = []
    T = []
    L1 = []
    L2 = []
    LT = []
    Y = []
    filelist = os.listdir(path)
    for i in range(0, len(filelist)):
    # for i in range(0, 1):
        filepath = os.path.join(path, filelist[i])
        logging.info("Loaded the file:"+filepath)
        if os.path.isfile(filepath):
            file = open(filepath, 'rb')
            testlist = json.loads(file.read())
            for map in testlist:
                commit = text2vec(map['commit'], False)
                issue = text2vec(map['issue'], True)
                title = text2vec(map['issuetitle'], False)
                L1.append(len(commit))
                X1.append(commit)
                L2.append(len(issue))
                X2.append(issue)
                LT.append(len(title))
                T.append(title)
                Y.append(float(map['type']))
            file.close()
    return X1, X2, T, L1, L2, LT, Y


# shape=[batch_size, None]
def make_batches(data, batch_size):
    X1, X2, T, L1, L2, LT, Y = data
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

    dataT = np.array(T[: batch_size*num_batches])
    dataT = np.reshape(dataT, [batch_size, num_batches])
    data_batchesT = np.split(dataT, num_batches, axis=1)  #  list
    data_batchesT_rs = []
    for d3t in data_batchesT:
        sub_batch = []
        maxD = 0
        for d in d3t:
            for dt in d:
                maxD = max(maxD, len(dt))
        for d in d3t:
            for dt in d:
                todo = maxD - len(dt)
                for index in range(todo):
                    dt.append(np.zeros(VECTOR_SIZE))
                sub_batch.append(np.array(dt))
        data_batchesT_rs.append(np.array(sub_batch))

    len1 = np.array(L1[: batch_size*num_batches])
    len1 = np.reshape(len1, [batch_size, num_batches])
    len_batches1 = np.split(len1, num_batches, axis=1)
    len_batches1 = np.reshape(np.array(len_batches1), [num_batches, BATCH_SIZE])

    len2 = np.array(L2[: batch_size * num_batches])
    len2 = np.reshape(len2, [batch_size, num_batches])
    len_batches2 = np.split(len2, num_batches, axis=1)
    len_batches2 = np.reshape(np.array(len_batches2), [num_batches, BATCH_SIZE])

    lenT = np.array(LT[: batch_size * num_batches])
    lenT = np.reshape(lenT, [batch_size, num_batches])
    len_batchesT = np.split(lenT, num_batches, axis=1)
    len_batchesT = np.reshape(np.array(len_batchesT), [num_batches, BATCH_SIZE])

    label = np.array(Y[: batch_size*num_batches])
    label = np.reshape(label, [batch_size, num_batches])
    label_batches = np.split(label, num_batches, axis=1)
    return list(zip(data_batches1_rs, data_batches2_rs, data_batchesT_rs, len_batches1, len_batches2, len_batchesT, label_batches))


class MyModel(object):
    def __init__(self, is_training, batch_size):
        self.batch_size = batch_size

        self.input1 = tf.placeholder(tf.float64, [BATCH_SIZE, None, VECTOR_SIZE])
        self.input2 = tf.placeholder(tf.float64, [BATCH_SIZE, None, VECTOR_SIZE])
        self.inputT = tf.placeholder(tf.float64, [BATCH_SIZE, None, VECTOR_SIZE])
        self.len1 = tf.placeholder(tf.int64, [BATCH_SIZE, ])
        self.len2 = tf.placeholder(tf.int64, [BATCH_SIZE, ])
        self.lent = tf.placeholder(tf.int64, [BATCH_SIZE, ])
        self.target = tf.placeholder(tf.float64, [BATCH_SIZE, 1])

        with tf.variable_scope("commit"):
            outputs1, states1 = self.RNN(self.input1, self.len1, is_training)
            tf.check_numerics(outputs1, 'output1 error')
        with tf.variable_scope("issue"):
            outputs2, states2 = self.RNN(self.input2, self.len2, is_training)
            tf.check_numerics(outputs2, 'output1 error')
        with tf.variable_scope("title"):
            outputs3, states3 = self.RNN(self.inputT, self.lent, is_training)
            tf.check_numerics(outputs3, 'output1 error')

        newoutput1 = states1[-1].h
        newoutput2 = states2[-1].h
        newoutput3 = states3[-1].h
        tf.check_numerics(newoutput1, 'newoutput1 error')
        tf.check_numerics(newoutput2, 'newoutput2 error')
        tf.check_numerics(newoutput3, 'newoutput3 error')

        # Define loss and optimizer
        self.cos_score = self.getScore(newoutput1, newoutput2, newoutput3)
        tf.check_numerics(self.cos_score, 'cos error')
        self.loss_op = self.getLoss(self.cos_score, self.target)
        tf.check_numerics(self.loss_op, 'loss_op error')

        if not is_training:
            return

        optimizer = tf.train.AdamOptimizer(learning_rate=LEARNING_RATE)
        self.train_op = optimizer.minimize(self.loss_op)

    def getScore(self, state1, state2, state3):
        pooled_len_1 = tf.sqrt(tf.reduce_sum(state1 * state1, 1))
        pooled_len_2 = tf.sqrt(tf.reduce_sum(state2 * state2, 1))
        pooled_mul_12 = tf.reduce_sum(state1 * state2, 1)
        score1 = tf.div(pooled_mul_12, pooled_len_1 * pooled_len_2 + 1e-8, name="scores1")  # +1e-8 avoid 'len_1/len_2 == 0'
        score1 = tf.reshape(score1, [BATCH_SIZE, 1])

        pooled_len_3 = tf.sqrt(tf.reduce_sum(state3 * state3, 1))
        pooled_mul_13 = tf.reduce_sum(state1 * state3, 1)
        score2 = tf.div(pooled_mul_13, pooled_len_1 * pooled_len_3 + 1e-8, name="scores2")  # +1e-8 avoid 'len_1/len_2 == 0'
        score2 = tf.reshape(score2, [BATCH_SIZE, 1])

        score = tf.concat([score1, score2], 1)
        score = tf.reduce_max(score, 1)
        return tf.reshape(score, [BATCH_SIZE, 1])

    #  |t - cossimilar(state1, state2)|
    def getLoss(self, score, t):
        rs = t - score
        rs = tf.abs(rs)
        return tf.reduce_sum(rs)

    def RNN(self, input_data, seq_len, is_training):
        dropout_keep_prob = LSTM_KEEP_PROB if is_training else 1.0
        lstm_cells = [
            tf.nn.rnn_cell.DropoutWrapper(tf.nn.rnn_cell.BasicLSTMCell(HIDDEN_SIZE), output_keep_prob=dropout_keep_prob)
            for _ in range(1)
        ]
        rnn_cell = tf.nn.rnn_cell.MultiRNNCell(lstm_cells)
        outputs, state = tf.nn.dynamic_rnn(rnn_cell, input_data, sequence_length=seq_len, dtype=tf.float64)
        return outputs, state


def run_epoch(session, model, batches, step):
    # session.run(model.init_state)
    for x1, x2, t, l1, l2, lt, y in batches:
        loss, _ = session.run([model.loss_op, model.train_op],
                           feed_dict={model.input1: x1, model.input2: x2, model.inputT: t, model.len1: l1, model.len2: l2, model.lent: lt, model.target: y})
        logging.info("At the step %d, the loss is %f" % (step, loss))


def test_epoch(session, model, batches, step):
    # session.run(model.init_state)
    temp = []
    total_correct = 0
    total_tests = len(batches) * BATCH_SIZE
    for x11, x21, t1, l11, l21, lt1, y1 in batches:
        score, loss = session.run([model.cos_score, model.loss_op],
                                feed_dict={model.input1: x11, model.input2: x21, model.inputT: t1, model.len1: l11, model.len2: l21, model.lent: lt1,
                                           model.target: y1})
        temp.append(loss)
        total_correct = total_correct + get_correct(score, y1)
    logging.info("At the test %d, the avg loss is %f, the accuracy is %f" % (step, np.mean(np.array(temp)), float(total_correct) / total_tests))
    if (float(total_correct) / total_tests) > MAX_RECORD['acc']:
        MAX_RECORD['step'] = step
        MAX_RECORD['acc'] = float(total_correct) / total_tests
    logging.info("MAX is at step %d: %f" % (MAX_RECORD['step'], MAX_RECORD['acc']))


def get_correct(score, target):
    result = 0
    zeros = 0
    ones = 0
    for i in range(len(target)):
        if target[i][0] == 1 and score[i][0] > 0.5:
            result = result + 1
            ones = ones + 1
        elif target[i][0] == 0 and score[i][0] < 0.5:
            result = result + 1
            zeros = zeros + 1
    logging.info("%d(0s) : %d(1s)" % (zeros, ones))
    #
    # for onescore in rs:
    #     if onescore[0] < 0.5:
    #         result = result + 1
    return result


def main():
    train_batches = make_batches(read_data(path='./train%d' % REPO_ID), BATCH_SIZE)
    test_batches = make_batches(read_data(path="./testset%d" % REPO_ID), BATCH_SIZE)

    with tf.variable_scope("rnn_model", reuse=None):
        train_model = MyModel(True, BATCH_SIZE)
    with tf.variable_scope("rnn_model", reuse=True):
        test_model = MyModel(False, BATCH_SIZE)

    init = tf.global_variables_initializer()
    with tf.Session() as sess:
        saver = tf.train.Saver()
        sess.run(init)

        for step in range(TRAIN_ITERS):
            logging.info("Step: " + str(step))
            run_epoch(session=sess, model=train_model, batches=train_batches, step=step)
            test_epoch(session=sess, model=test_model, batches=test_batches, step=step)
        saver.save(sess, 'rnnmodel/adam/rnn', global_step=TRAIN_ITERS)
        logging.info("Optimization Finished!")


if __name__ == "__main__":
    main()
