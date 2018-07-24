# -*- coding: UTF-8 -*-

import logging
import os
import json
import nocodeRepoInfo
from gensim.models import TfidfModel
from gensim.corpora import Dictionary
from gensim.matutils import cossim

logging.basicConfig(format='%(asctime)s : %(levelname)s : %(message)s', level=logging.INFO)

TRAIN_ITERS = 300
REPO_ID = nocodeRepoInfo.REPO_MAP[nocodeRepoInfo.USE_REPO_INDEX]['id']


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
            res.extend(json.loads(file.read()))
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


def main():
    links = read_data(path='./frtrain%d' % REPO_ID)
    logging.info("Size: "+str(len(links)))
    link_list = []
    for link in links:
        type = link['type']
        val = max(getTextSim(link['commitText'], link['issueText']), getCodeSim(link['commitCode'], link['issueCode']))
        link_list.append({'type': type, 'val': val})
    res = json.dumps(link_list, indent=4)
    trainSet = open('./frlink%d/all.dat' % REPO_ID, "w")
    trainSet.write(res)
    trainSet.close()
    logging.info("Build Finished!")


if __name__ == "__main__":
    main()
