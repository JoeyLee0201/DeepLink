# -*- coding: UTF-8 -*-

from gensim.models import word2vec

import logging

logging.basicConfig(format='%(asctime)s : %(levelname)s : %(message)s', level=logging.INFO)

VECTOR_SIZE = 100
REPO_ID = 13421878

# sentences1 = word2vec.Text8Corpus("test/commit50904245.dat")
# model1 = word2vec.Word2Vec(sentences1, size=VECTOR_SIZE)
# model1.save("test/commit50904245.model")
#
# sentences2 = word2vec.Text8Corpus("test/issue50904245.dat")
# model2 = word2vec.Word2Vec(sentences2, size=VECTOR_SIZE)
# model2.save("test/issue50904245.model")

sentences3 = word2vec.Text8Corpus("corpus/nocode%d.dat" % REPO_ID)
model3 = word2vec.Word2Vec(sentences3, size=VECTOR_SIZE, sg=1, hs=1,  iter=50)
model3.save("test/nocode%d.model" % REPO_ID)
