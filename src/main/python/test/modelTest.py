# -*- coding: UTF-8 -*-

import numpy as np

from gensim.models.doc2vec import Doc2Vec
from gensim.models import word2vec

import logging

logging.basicConfig(format='%(asctime)s : %(levelname)s : %(message)s', level=logging.INFO)


def getVecs(model, corpus, size):
    vecs = [np.array(model.docvecs[z.tags[0]].reshape(1, size)) for z in corpus]
    return np.concatenate(vecs)


def testD():
    model_dm = Doc2Vec.load("text.model")
    test_text = ['fix', 'bug']
    inferred_vector_dm = model_dm.infer_vector(test_text)
    print inferred_vector_dm
    sims = model_dm.docvecs.most_similar([inferred_vector_dm], topn=10)
    return sims


if __name__ == '__main__':
    # model_dm = Doc2Vec.load("nocodedoc50904245.model")
    # test_text = []
    # inferred_vector_dm = model_dm.infer_vector(test_text)
    # print inferred_vector_dm
    # sims = model_dm.docvecs.most_similar([inferred_vector_dm], topn=10)
    # print sims
    wordModel = word2vec.Word2Vec.load('nocode50904245.model')
    print wordModel.wv.index2word.index('fix')
    print wordModel.wv.index2word[19]

    print wordModel.wv.index2word.index('bug')
    print wordModel[wordModel.wv.index2word[79]]
    print wordModel['bug']

    print wordModel.wv.index2word.index('---')
