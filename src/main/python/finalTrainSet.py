# -*- coding: UTF-8 -*-

from database import linkOperator, mysqlOperator
from gitresolver import gitResolver
from preprocessor import preprocessor
from preprocessor import frpreprocesser
import json
import sys
import random
import nocodeRepoInfo
import traceback
import os

reload(sys)
sys.setdefaultencoding('utf-8')


def getRandomFalse(falseTable, start, end, size):
    links = linkOperator.selectInScope((falseTable, start, end))
    return random.sample(links, size)


def buildTrainSet(trueTable, falseTable, repoId, repoPath, trueGap, falseGap, trueCount, falseCount):
    trueStart = 1
    falseStart = 1
    textCorpus = open('frcorpus/frtext%d.dat' % repoId, "w")
    codeCorpus = open('frcorpus/frcode%d.dat' % repoId, "w")
    trueLinkList = linkOperator.selectInScope((trueTable, trueStart, trueStart + trueCount))
    falseLinkList = getRandomFalse(falseTable, falseStart, falseStart + falseGap, falseCount)

    index = 0
    repo = gitResolver.GitResolver(repoPath)
    try:
        while len(trueLinkList) > 0 and len(falseLinkList) > 0:
            print 'true: ', trueStart, ' to ', trueStart + trueCount
            print 'false: ', falseStart, ' to ', falseStart + falseCount
            my_linkList = []
            fr_linkList = []
            for trueLink in trueLinkList:
                commit = repo.getOneCommit(trueLink[1])
                issue = mysqlOperator.selectOneIssue(trueLink[2])
                if issue is None:
                    continue

                my_res = {}
                my_res['type'] = 1
                my_res['commit'] = commit.message.decode('utf-8')
                my_res['issuetitle'] = issue[4].decode('utf-8')
                # issue body
                if issue[5]:
                    my_res['issue'] = issue[5].decode('utf-8')
                    issueCodes = []
                    bodycode = preprocessor.getIssueCode(my_res['issue'])
                    if len(bodycode):
                        issueCodes.append(bodycode)
                    my_res['issuecode'] = issueCodes
                else:
                    my_res['issue'] = ''
                    my_res['issuecode'] = []

                diffs = repo.getOneDiff(commit)
                diffCodes = []
                for diff in diffs:
                    diffCode = preprocessor.processDiffCode(diff.diff)
                    if len(diffCode):
                        diffCodes.append(diffCode)
                my_res['commitcode'] = diffCodes
                my_linkList.append(my_res)

                comments = mysqlOperator.selectCommentInOneIssue(trueLink[2])
                try:
                    files = repo.getFiles(trueLink[1])
                except:
                    print 'File Fail 1:', trueLink[1]
                    continue

                fr_res = {}
                fr_res['type'] = 1
                fr_res['issueText'] = []
                # issue body
                if issue[5]:
                    fr_res['issueCode'] = frpreprocesser.extractCode(issue[5].decode('utf-8'))
                    fr_res['issueText'].append(frpreprocesser.extractText(issue[5].decode('utf-8')))  # body
                else:
                    fr_res['issueCode'] = []
                fr_res['issueText'].append(frpreprocesser.extractText(issue[4].decode('utf-8')))  # title
                for comment in comments:
                    fr_res['issueText'].append(frpreprocesser.extractText(comment[4].decode('utf-8')))
                fr_res['commitText'] = []
                fr_res['commitCode'] = []
                fr_res['commitText'].append(frpreprocesser.extractText(commit.message.decode('utf-8')))
                for changeFile in files:
                    if not changeFile['path'].endswith('.java'):
                        try:
                            fr_res['commitText'].append(frpreprocesser.extractText(changeFile['text'].decode('utf-8')))
                        except:
                            print trueLink[1], ':', changeFile['path']
                    else:
                        codes = frpreprocesser.extractCode(changeFile['text'].decode('utf-8'))
                        for code in codes:
                            if code in fr_res['issueCode']:
                                fr_res['commitCode'].extend(codes)
                                break
                fr_linkList.append(fr_res)
                writeToCorpus(textCorpus, codeCorpus, fr_res['commitText'], fr_res['commitCode'])
                writeToCorpus(textCorpus, codeCorpus, fr_res['issueText'], fr_res['issueCode'])

            for falseLink in falseLinkList:
                commit = repo.getOneCommit(falseLink[1])
                issue = mysqlOperator.selectOneIssue(falseLink[2])
                if issue is None:
                    continue

                my_res = {}
                my_res['type'] = 0
                my_res['commit'] = commit.message.decode('utf-8')
                my_res['issuetitle'] = issue[4].decode('utf-8')
                # issue body
                if issue[5]:
                    my_res['issue'] = issue[5].decode('utf-8')
                    issueCodes = []
                    bodycode = preprocessor.getIssueCode(my_res['issue'])
                    if len(bodycode):
                        issueCodes.append(bodycode)
                    my_res['issuecode'] = issueCodes
                else:
                    my_res['issue'] = ''
                    my_res['issuecode'] = []

                diffs = repo.getOneDiff(commit)
                diffCodes = []
                for diff in diffs:
                    diffCode = preprocessor.processDiffCode(diff.diff)
                    if len(diffCode):
                        diffCodes.append(diffCode)
                my_res['commitcode'] = diffCodes
                my_linkList.append(my_res)

                comments = mysqlOperator.selectCommentInOneIssue(falseLink[2])
                try:
                    files = repo.getFiles(falseLink[1])
                except:
                    print 'File Fail 0:', falseLink[1]
                    continue

                fr_res = {}
                fr_res['type'] = 0
                fr_res['issueText'] = []
                # issue body
                if issue[5]:
                    fr_res['issueCode'] = frpreprocesser.extractCode(issue[5].decode('utf-8'))
                    fr_res['issueText'].append(frpreprocesser.extractText(issue[5].decode('utf-8')))  # body
                else:
                    fr_res['issueCode'] = []
                fr_res['issueText'].append(frpreprocesser.extractText(issue[4].decode('utf-8')))  # title
                for comment in comments:
                    fr_res['issueText'].append(frpreprocesser.extractText(comment[4].decode('utf-8')))
                fr_res['commitText'] = []
                fr_res['commitCode'] = []
                fr_res['commitText'].append(frpreprocesser.extractText(commit.message.decode('utf-8')))
                for changeFile in files:
                    if not changeFile['path'].endswith('.java'):
                        try:
                            fr_res['commitText'].append(frpreprocesser.extractText(changeFile['text'].decode('utf-8')))
                        except:
                            print trueLink[1], ':', changeFile['path']
                    else:
                        codes = frpreprocesser.extractCode(changeFile['text'].decode('utf-8'))
                        for code in codes:
                            if code in fr_res['issueCode']:
                                fr_res['commitCode'].extend(codes)
                                break
                fr_linkList.append(fr_res)
                writeToCorpus(textCorpus, codeCorpus, fr_res['commitText'], fr_res['commitCode'])
                writeToCorpus(textCorpus, codeCorpus, fr_res['issueText'], fr_res['issueCode'])

            index += 1
            res = json.dumps(my_linkList, encoding="utf-8", indent=4)
            trainSet = open('%s/codetrain%d-%d.dat' % (my_folder, repoId, index), "w")
            trainSet.write(res)
            trainSet.close()
            print '%s/codetrain%d-%d.dat' % (my_folder, repoId, index), 'Over'
            fres = json.dumps(fr_linkList, encoding="utf-8", indent=4)
            ftrainSet = open('%s/traincase%d-%d.dat' % (fr_folder, repoId, index), "w")
            ftrainSet.write(fres)
            ftrainSet.close()
            print '%s/traincase%d-%d.dat' % (fr_folder, repoId, index), 'Over'

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
    fr_folder = os.getcwd() + ('/finalFr%d' % repo_id)
    my_folder = os.getcwd() + ('/finalMy%d' % repo_id)
    if not os.path.exists(fr_folder):
        os.makedirs(fr_folder)
    if not os.path.exists(my_folder):
        os.makedirs(my_folder)
    if not os.path.exists(os.getcwd() + 'frcorpus'):
        os.makedirs(os.getcwd() + 'frcorpus')
    buildTrainSet('true_link_%d' % repo_id, 'false_link_%d' % repo_id, repo_id, repo_path,
                  nocodeRepoInfo.REPO_MAP[nocodeRepoInfo.USE_REPO_INDEX]['trueGap'],
                  nocodeRepoInfo.REPO_MAP[nocodeRepoInfo.USE_REPO_INDEX]['falseGap'],
                  nocodeRepoInfo.REPO_MAP[nocodeRepoInfo.USE_REPO_INDEX]['trueCount'],
                  nocodeRepoInfo.REPO_MAP[nocodeRepoInfo.USE_REPO_INDEX]['falseCount'])