# -*- coding: UTF-8 -*-

import logging
import json
import nocodeRepoInfo

logging.basicConfig(format='%(asctime)s : %(levelname)s : %(message)s', level=logging.INFO)
REPO_ID = nocodeRepoInfo.REPO_MAP[nocodeRepoInfo.USE_REPO_INDEX]['id']


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
        precision = TP/(TP+FP)
        recall = TP/(TP+FN)
        f_measure = (2*precision*recall)/(precision + recall)
        if recall >= ITR:
            if (f_measure > F) or (f_measure == F and recall > RMax):
                LThres = ThresVal
                RMax = recall
                F = f_measure
        ThresVal = ThresVal + Step
        logging.info(ThresVal)
    return LThres


def read_data(path):
    with open(path, 'rb') as f:
        res = json.loads(f.read())
    return res


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
    precision = float(TP) / (TP + FP)
    recall = float(TP) / (TP + FN)
    f_measure = (2 * precision * recall) / (precision + recall)
    logging.info("precision:%f  recall:%f  f_measure:%f" % (precision, recall, f_measure))


def main():
    links = read_data(path='./frlink%d/all.dat' % REPO_ID)
    logging.info("Size: "+str(len(links)))
    train = int(len(links)*0.8)
    trainset = links[:train]
    testset = links[train:]
    t = learn(trainset, 0.88)
    res = getRes(testset, t)
    logging.info(t)
    logging.info(res)
    evaluation(testset, t)
    logging.info("Finished!")


if __name__ == "__main__":
    main()
