# -*- coding: UTF-8 -*-

import logging
import json
import nocodeRepoInfo
import os
from gensim.models import TfidfModel
from gensim.corpora import Dictionary
from gensim.matutils import cossim

logging.basicConfig(format='%(asctime)s : %(levelname)s : %(message)s', level=logging.INFO)
REPO_ID = nocodeRepoInfo.REPO_MAP[nocodeRepoInfo.USE_REPO_INDEX]['id']
TRAIN_ITERS = 300


def getCorpus(path):
    corpus_list = []
    with open(path, 'rb') as f:
        lines = f.readlines()
        for sentence in lines:
            words = sentence.decode('utf8').split(" ")
            sentence_segment = []
            for word in words:
                if word.strip() != '':
                    sentence_segment.append(word.strip())
            corpus_list.append(sentence_segment)
    return corpus_list


code_dataset = getCorpus("frcorpus/text%d.dat" % REPO_ID)
text_dataset = getCorpus("frcorpus/code%d.dat" % REPO_ID)
code_dct = Dictionary(code_dataset)
text_dct = Dictionary(text_dataset)
code_corpus = [code_dct.doc2bow(line) for line in code_dataset]  # convert corpus to BoW format
text_corpus = [text_dct.doc2bow(line) for line in text_dataset]  # convert corpus to BoW format
code_model = TfidfModel(code_corpus)
code_model.save("frcorpus/code%d.model" % REPO_ID)
text_model = TfidfModel(text_corpus)
text_model.save("frcorpus/text%d.model" % REPO_ID)


def read_data(path):
    res = []
    filelist = os.listdir(path)
    for i in range(0, len(filelist)):
        filepath = os.path.join(path, filelist[i])
        logging.info("Loaded the file:"+filepath)
        if os.path.isfile(filepath):
            file = open(filepath, 'rb')
            testlist = json.loads(file.read())
            res.extend(testlist)
            file.close()
    return res


def getSim(vec1, vec2):
    return cossim(vec1, vec2)


def getTextSim(commitText, issueText):
    res = 0
    for cText in commitText:
        cVec = text_model[text_dct.doc2bow(cText)]
        for iText in issueText:
            iVec = text_model[text_dct.doc2bow(iText)]
            res = max(res, getSim(cVec, iVec))
    return res


def getCodeSim(commitCode, issueCode):
    cVec = code_model[code_dct.doc2bow(commitCode)]
    iVec = code_model[code_dct.doc2bow(issueCode)]
    return getSim(cVec, iVec)


def learn(list, ITR):
    ThresVal = 0.0
    Step = 0.01
    LThres = 0.0
    F = 0.0
    RMax = ITR
    while ThresVal <= 1:
        logging.info(ThresVal)
        TP = 0
        FP = 0
        FN = 0
        for link in list:
            if link['val'] >= ThresVal:
                if link['type'] == 1:
                    TP += 1
                else:
                    FP += 1
            else:
                if link['type'] == 1:
                    FN += 1
        precision = TP/(TP+FP+1e-8)
        recall = TP/(TP+FN+1e-8)
        f_measure = (2*precision*recall)/(precision + recall+1e-8)
        if recall >= ITR:
            if (f_measure > F) or (f_measure == F and recall > RMax):
                LThres = ThresVal
                RMax = recall
                F = f_measure
        ThresVal = ThresVal + Step
        logging.info(ThresVal)
    return LThres


def getRes(test_set, t):
    size = len(test_set)
    right = 0.0
    for link in test_set:
        if link['type'] == 1 and link['val'] >= t:
            right += 1
        elif link['type'] == 0 and link['val'] < t:
            right += 1
    return right/size


def evaluation(test_set, t):
    TP = 0
    FP = 0
    FN = 0
    for link in test_set:
        if link['val'] >= t:
            if link['type'] == 1:
                TP += 1
            else:
                FP += 1
        else:
            if link['type'] == 1:
                FN += 1
    precision = float(TP) / (TP + FP+1e-8)
    recall = float(TP) / (TP + FN+1e-8)
    f_measure = (2 * precision * recall) / (precision + recall+1e-8)
    logging.info("precision:%f  recall:%f  f_measure:%f" % (precision, recall, f_measure))


def build(path):
    res_folder = os.getcwd() + ('/finalFrTrain%d' % REPO_ID)
    if not os.path.exists(res_folder):
        os.makedirs(res_folder)
    test_folder = os.getcwd() + ('/finalFrTest%d' % REPO_ID)
    if not os.path.exists(test_folder):
        os.makedirs(test_folder)

    filelist = os.listdir(path)
    for i in range(0, len(filelist)):
        filepath = os.path.join(path, filelist[i])
        logging.info("Loaded the file:" + filepath)
        if os.path.isfile(filepath):
            file = open(filepath, 'rb')
            links = json.loads(file.read())
            index = int(getIndex(filelist[i]))
            link_list = []
            for link in links:
                type = link['type']
                val = max(getTextSim(link['commitText'], link['issueText']),
                          getCodeSim(link['commitCode'], link['issueCode']))
                link_list.append({'type': type, 'val': val})
            res = json.dumps(link_list, indent=4)
            trainSet = open('%s/frtrain%d-%d.dat' % (res_folder, REPO_ID, index), "w")
            trainSet.write(res)
            trainSet.close()
            file.close()


def getIndex(s):
    start = s.find("-")
    return s[start + 1:-4]


def main():
    trainset = read_data(path='./finalFrTrain%d' % REPO_ID)
    testset = read_data(path='./finalFrTest%d' % REPO_ID)
    t = learn(trainset, 0.88)
    res = getRes(testset, t)
    logging.info(t)
    logging.info(res)
    evaluation(testset, t)
    logging.info("Finished!")


if __name__ == "__main__":
    input = 1
    if input == 1:
        build('./finalFr%d' % REPO_ID)
    else:
        main()
