# -*- coding: UTF-8 -*-

from preprocessor import preprocessor
from database import linkOperator
from gensim.models.doc2vec import Doc2Vec

import logging
import os
import json

logging.basicConfig(format='%(asctime)s : %(levelname)s : %(message)s', level=logging.INFO)

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
    filelist = os.listdir(path)
    for i in range(0, len(filelist)):
        filepath = os.path.join(path, filelist[i])
        if os.path.isfile(filepath):
            file = open(filepath, 'rb')
            testlist = json.loads(file.read())
            for map in testlist:
                commit = text2vec(map['commit'], False)
                issue = text2vec(map['issue'], True)
                linkOperator.insertCossim((map['type'], cosine_similarity(commit, issue)))
            file.close()


read_data()