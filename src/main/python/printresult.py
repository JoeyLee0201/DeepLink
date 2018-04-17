# -*- coding: UTF-8 -*-

from gensim.models import word2vec

import logging

logging.basicConfig(format='%(asctime)s : %(levelname)s : %(message)s', level=logging.INFO)

model = word2vec.Word2Vec.load('words.model')

print "model : ",model

try: 
    y1 = model.similarity("performance","bug") 
except KeyError: 
    y1 = 0 
print "performance - bug:{}\n".format(y1)

y2 = model.most_similar("performance",topn=20)
print("like performance:\n") 
for word in y2: 
    print word[0], word[1]
print("*********\n") 

y3 = model.most_similar("bug",topn=20)
print("like bug:\n") 
for word in y3: 
    print word[0], word[1]
print("*********\n") 

y4 = model.most_similar("issue",topn=20)
print("like issue:\n") 
for word in y4: 
    print word[0], word[1]
print("*********\n") 