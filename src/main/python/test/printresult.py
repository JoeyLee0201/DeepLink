# -*- coding: UTF-8 -*-

from gensim.models import word2vec
from preprocessor import preprocessor

import logging

logging.basicConfig(format='%(asctime)s : %(levelname)s : %(message)s', level=logging.INFO)

model = word2vec.Word2Vec.load('nocode50904245-1.model')

try:
    y1 = model.similarity("performance","bug")
except KeyError:
    y1 = 0
print "performance - bug:{}\n".format(y1)

y2 = model.most_similar("fix", topn=20)
print("like fix:\n")
for word in y2:
    print word[0], word[1]
print("*********\n")

y3 = model.most_similar("bug", topn=20)
print("like bug:\n")
for word in y3:
    print word[0], word[1]
print("*********\n")

y4 = model.most_similar("issu", topn=20)
print("like issue:\n")
for word in y4:
    print word[0], word[1]
print("*********\n")

# sentences = preprocessor.preprocess('I fixed a bug. I fixed the issue. She like to sing a love song to the boy.')
# print model.wmdistance(sentences[0], sentences[1])
# print model.wmdistance(sentences[0], sentences[2])
# print model.wmdistance(sentences[1], sentences[2])