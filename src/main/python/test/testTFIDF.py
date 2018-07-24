# -*- coding: UTF-8 -*-

import logging
import os
import json
import nocodeRepoInfo
from gensim.models import TfidfModel
from gensim.corpora import Dictionary
from gensim.matutils import cossim
import math

logging.basicConfig(format='%(asctime)s : %(levelname)s : %(message)s', level=logging.INFO)
REPO_ID = nocodeRepoInfo.REPO_MAP[nocodeRepoInfo.USE_REPO_INDEX]['id']


def getCorpus(path):
    corpus_list = []
    with open(path, 'rb') as f:
        lines = f.readlines()
        for sentence in lines:
            words = sentence.split(" ")
            sentence_segment = []
            for word in words:
                if word.strip() != '':
                    sentence_segment.append(word.strip())
            corpus_list.append(sentence_segment)
    return corpus_list


code_dataset = getCorpus("../frcorpus/text%d.dat" % REPO_ID)
text_dataset = getCorpus("../frcorpus/code%d.dat" % REPO_ID)
code_dct = Dictionary(code_dataset)
text_dct = Dictionary(text_dataset)
code_corpus = [code_dct.doc2bow(line) for line in code_dataset]  # convert corpus to BoW format
text_corpus = [text_dct.doc2bow(line) for line in text_dataset]  # convert corpus to BoW format
code_model = TfidfModel(code_corpus)
code_model.save("../frcorpus/code%d.model" % REPO_ID)
text_model = TfidfModel(text_corpus)
text_model.save("../frcorpus/text%d.model" % REPO_ID)


def getSim(vec1, vec2):
    print vec1
    print vec2
    print cossim(vec1, vec2)
    print '============================================'


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


def main():
    t1 = [["issu", "ad", "javadocparsererrorstrategi", "extend", "bailerrorstrategi"]]
    t2 = [["issu",
                "ad",
                "abstractmoduletestsupport",
                "genericwhitespacechecktest",
                "parenpadchecktest",
                "filetabcharacterchecktest",
                "packageannotationchecktest",
                "now",
                "extend"
            ]]
    c1 = ["html", "svg", "mathml", "u+002f", "u+003", "u+002f", "singletontag"]
    c2 = ["auditeventdefaultformattertest", "auditev", "mock"]
    vec1 = text_model[text_dct.doc2bow(t1[0])]
    vec2 = text_model[text_dct.doc2bow(t2[0])]
    tc1 = 0
    tc2 = 0
    for t in vec1:
        tc1 = tc1 + t[1] * t[1]
    for t in vec2:
        tc2 = tc2 + t[1] * t[1]
    top = vec1[0][1] * vec2[0][1] + vec1[1][1] * vec2[3][1] + vec1[2][1] * vec2[4][1]
    print top / (math.sqrt(tc1) * math.sqrt(tc2))
    getTextSim(t1, t2)
    getCodeSim(c1, c2)
    getTextSim(t1, t1)
    getCodeSim(c1, c1)
    getCodeSim([], c1)


if __name__ == "__main__":
    main()
