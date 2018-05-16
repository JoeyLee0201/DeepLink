# -*- coding: UTF-8 -*-

import numpy as np  
  
from gensim.models.doc2vec import Doc2Vec, TaggedLineDocument

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
  
# if __name__ == '__main__':  
#     print 'start train'
#     x_train = get_datasest('corpusLabel.dat')  
#     print 'start model'
#     model_dm = train(x_train)  
#     print 'start test'
#     sims = test()  
#     for count, sim in sims:  
#         sentence = x_train[count]  
#         words = ''  
#         for word in sentence[0]:  
#             words = words + word + ' '  
#         print words, sim, len(sentence[0]) 


if __name__ == '__main__':  
    print '=============== text start train ==============='
    texts = TaggedLineDocument('corpus/text12983151.dat')
    textModel = Doc2Vec(texts, min_count=1, dm=0, window=5, size=100, sample=1e-3, negative=5, workers=4)
    textModel.save('text12983151.model')
    print '=============== text end train ==============='

    print '=============== code start train ==============='
    codes = TaggedLineDocument('corpus/code12983151.dat')
    codeModel = Doc2Vec(codes, min_count=1, dm=0, window=5, size=100, sample=1e-3, negative=5, workers=4)
    codeModel.save('code12983151.model')
    print '=============== code end train ==============='
