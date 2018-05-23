# -*- coding: UTF-8 -*-

from gensim.models.doc2vec import Doc2Vec
from preprocessor import preprocessor
import json
import os


def similarity(a_vect, b_vect):
    """计算两个向量余弦值
    Arguments:
        a_vect {[type]} -- a 向量
        b_vect {[type]} -- b 向量
    Returns:
        [type] -- [description]
    """
    dot_val = 0.0
    a_norm = 0.0
    b_norm = 0.0
    for a, b in zip(a_vect, b_vect):
        dot_val += a * b
        a_norm += a ** 2
        b_norm += b ** 2
    if a_norm == 0.0 or b_norm == 0.0:
        return -1
    else:
        return dot_val / ((a_norm * b_norm) ** 0.5)


textModel = Doc2Vec.load("text12983151.model")
codeModel = Doc2Vec.load("code12983151.model")

index = 0
while index < 3:
    linkList = []
    titleWords = preprocessor.preprocessToWord("test is for your parents")
    print type(textModel.infer_vector(titleWords))
    titelTextVec = textModel.infer_vector(titleWords).tolist()
    print type(titelTextVec[0])
    diffCode = preprocessor.processDiffCode("test is for your parents")
    commitCodeVec = codeModel.infer_vector(diffCode).tolist()
    linkList.append({'text': titelTextVec, 'code': commitCodeVec})
    linkList.append({'text': titelTextVec, 'code': commitCodeVec})
    index += 1

    # res = json.dumps(linkList, encoding="utf-8", indent=4)
    # trainSet = open('./train/traruanhincase%d.dat' % index, "w")
    # trainSet.write(res)
    # trainSet.close()

# path = './train'
# filelist = os.listdir(path)
# for i in range(0, len(filelist)):
#     filepath = os.path.join(path, filelist[i])
#     print filepath
#     if os.path.isfile(filepath):
#         file = open(filepath, 'r')
#         testlist = json.loads(file.read())
#         if len(testlist):
#             t0 = testlist[0]
#             t1 = testlist[1]
#             print similarity(t0['text'], t1['text'])
#         file.close()
