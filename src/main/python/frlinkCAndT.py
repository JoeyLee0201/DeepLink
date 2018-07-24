# -*- coding: UTF-8 -*-

from database import linkOperator, mysqlOperator
from gitresolver import gitResolver
from preprocessor import frpreprocesser

import logging
import traceback
import sys
import nocodeRepoInfo
import json
import random

reload(sys)
sys.setdefaultencoding('utf-8')

logging.basicConfig(format='%(asctime)s : %(levelname)s : %(message)s', level=logging.INFO)


def getRandomFalse(falseTable, start, end, size):
    links = linkOperator.selectInScope((falseTable, start, end))
    return random.sample(links, size)


def buildTrainSet(trueTable, falseTable, repoId, repoPath, trueGap, falseGap, trueCount, falseCount):
    trueStart = 1
    falseStart = 1
    textCorpus = open('frcorpus/text%d.dat' % repoId, "w")
    codeCorpus = open('frcorpus/code%d.dat' % repoId, "w")
    trueLinkList = linkOperator.selectInScope((trueTable, trueStart, trueStart + trueCount))
    falseLinkList = getRandomFalse(falseTable, falseStart, falseStart + falseGap, falseCount)

    index = 0
    repo = gitResolver.GitResolver(repoPath)
    try:
        while len(trueLinkList) > 0 and len(falseLinkList) > 0:
            print 'true: ', trueStart, ' to ', trueStart + trueCount
            print 'false: ', falseStart, ' to ', falseStart + falseCount
            linkList = []
            for trueLink in trueLinkList:
                commit = repo.getOneCommit(trueLink[1])
                issue = mysqlOperator.selectOneIssue(trueLink[2])
                if issue is None:
                    continue
                comments = mysqlOperator.selectCommentInOneIssue(trueLink[2])
                try:
                    files = repo.getFiles(trueLink[1])
                except:
                    print 'File Fail 1:', trueLink[1]
                    continue

                res = {}
                res['type'] = 1
                res['issueText'] = []
                # issue body
                if issue[5]:
                    res['issueCode'] = frpreprocesser.extractCode(issue[5].decode('utf-8'))
                    res['issueText'].append(frpreprocesser.extractText(issue[5].decode('utf-8')))  # body
                else:
                    res['issueCode'] = []
                res['issueText'].append(frpreprocesser.extractText(issue[4].decode('utf-8')))  # title
                for comment in comments:
                    res['issueText'].append(frpreprocesser.extractText(comment[4].decode('utf-8')))
                res['commitText'] = []
                res['commitCode'] = []
                res['commitText'].append(frpreprocesser.extractText(commit.message.decode('utf-8')))
                for changeFile in files:
                    if not changeFile['path'].endswith('.java'):
                        try:
                            res['commitText'].append(frpreprocesser.extractText(changeFile['text'].decode('utf-8')))
                        except:
                            print trueLink[1], ':', changeFile['path']
                    else:
                        codes = frpreprocesser.extractCode(changeFile['text'].decode('utf-8'))
                        for code in codes:
                            if code in res['issueCode']:
                                res['commitCode'].extend(codes)
                                break
                linkList.append(res)
                writeToCorpus(textCorpus, codeCorpus, res['commitText'], res['commitCode'])
                writeToCorpus(textCorpus, codeCorpus, res['issueText'], res['issueCode'])

            for falseLink in falseLinkList:
                commit = repo.getOneCommit(falseLink[1])
                issue = mysqlOperator.selectOneIssue(falseLink[2])
                if issue is None:
                    continue
                comments = mysqlOperator.selectCommentInOneIssue(falseLink[2])
                try:
                    files = repo.getFiles(falseLink[1])
                except:
                    print 'File Fail 0:', falseLink[1]
                    continue

                res = {}
                res['type'] = 0
                res['issueText'] = []
                # issue body
                if issue[5]:
                    res['issueCode'] = frpreprocesser.extractCode(issue[5].decode('utf-8'))
                    res['issueText'].append(frpreprocesser.extractText(issue[5].decode('utf-8')))  # body
                else:
                    res['issueCode'] = []
                res['issueText'].append(frpreprocesser.extractText(issue[4].decode('utf-8')))  # title
                for comment in comments:
                    res['issueText'].append(frpreprocesser.extractText(comment[4].decode('utf-8')))
                res['commitText'] = []
                res['commitCode'] = []
                res['commitText'].append(frpreprocesser.extractText(commit.message.decode('utf-8')))
                for changeFile in files:
                    if not changeFile['path'].endswith('.java'):
                        try:
                            res['commitText'].append(frpreprocesser.extractText(changeFile['text'].decode('utf-8')))
                        except:
                            print trueLink[1], ':', changeFile['path']
                    else:
                        codes = frpreprocesser.extractCode(changeFile['text'].decode('utf-8'))
                        for code in codes:
                            if code in res['issueCode']:
                                res['commitCode'].extend(codes)
                                break
                linkList.append(res)
                writeToCorpus(textCorpus, codeCorpus, res['commitText'], res['commitCode'])
                writeToCorpus(textCorpus, codeCorpus, res['issueText'], res['issueCode'])

            index += 1
            res = json.dumps(linkList, encoding="utf-8", indent=4)
            trainSet = open('./frtrain%d/traincase%d-%d.dat' % (repoId, repoId, index), "w")
            trainSet.write(res)
            trainSet.close()
            print './frtrain%d/traincase%d-%d.dat' % (repoId, repoId, index), 'Over'

            trueStart += trueGap
            falseStart += falseGap
            trueLinkList = linkOperator.selectInScope((trueTable, trueStart, trueStart + trueCount))
            falseLinkList = getRandomFalse(falseTable, falseStart, falseStart + falseGap, falseCount)
    except IOError, e:
        print "***", e
        print traceback.format_exc()
    finally:
        textCorpus.close()
        codeCorpus.close()
    mysqlOperator.close()
    linkOperator.close()


def writeToCorpus(text_corpus, code_corpus, texts, code):
    for text in texts:
        writeOneDoc(text_corpus, text)
    writeOneDoc(code_corpus, code)


def writeOneDoc(corpus, word_list):
    if len(word_list) > 0:
        for word in word_list:
            corpus.write(word.encode('utf-8'))
            corpus.write(" ")
        corpus.write("\n")


if __name__ == '__main__':
    repo_id = nocodeRepoInfo.REPO_MAP[nocodeRepoInfo.USE_REPO_INDEX]['id']
    repo_path = nocodeRepoInfo.REPO_MAP[nocodeRepoInfo.USE_REPO_INDEX]['path']
    buildTrainSet('true_link_%d' % repo_id, 'false_link_%d' % repo_id, repo_id, repo_path,
                  nocodeRepoInfo.REPO_MAP[nocodeRepoInfo.USE_REPO_INDEX]['trueGap'],
                  nocodeRepoInfo.REPO_MAP[nocodeRepoInfo.USE_REPO_INDEX]['falseGap'],
                  nocodeRepoInfo.REPO_MAP[nocodeRepoInfo.USE_REPO_INDEX]['trueCount'],
                  nocodeRepoInfo.REPO_MAP[nocodeRepoInfo.USE_REPO_INDEX]['falseCount'])
