# -*- coding: UTF-8 -*-

from database import linkOperator, mysqlOperator
from gensim.models.doc2vec import Doc2Vec
from preprocessor import preprocessor
from gitresolver import gitResolver
import re
import traceback
import json


def getPath(s):
    temp = re.sub(r'https://github.com/', '', s, 0, re.I)
    return "/home/fdse/data/prior_repository/" + temp


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


repoMap = {}
repoMap[12983151L] = gitResolver.GitResolver('/home/fdse/data/prior_repository/openhab/openhab1-addons')

# repos = mysqlOperator.selectAllHighRepository()
# for repo in repos:
#     print type(repo[0])
    # try:
    #     repoMap[repo[0]] = gitResolver.GitResolver(getPath(repo[1]))
    # except:
    #     repoMap[repo[0]] = None

# TRUE_LINK_TOTAL = linkOperator.count('true_link')
# FALSE_LINK_TOTAL = linkOperator.count('false_link')
TRUE_GAP = 100
FALSE_GAP = 10000

trueStart = 1
falseStart = 1
textModel = Doc2Vec.load("text12983151.model")
codeModel = Doc2Vec.load("code12983151.model")

trueLinkList = linkOperator.selectInScope(('sql_true_link', trueStart, trueStart+TRUE_GAP))
falseLinkList = linkOperator.selectInScope(('sql_false_link', falseStart, falseStart+FALSE_GAP))

index = 0
while len(trueLinkList) > 0 and len(falseLinkList) > 0:
    print 'true: ', trueStart, ' to ', trueStart+TRUE_GAP
    print 'false: ', falseStart, ' to ', falseStart+FALSE_GAP
    linkList = []
    for trueLink in trueLinkList:
        tempMap = {}
        temp['type'] = 1
        repo = repoMap[trueLink[0]]
        commit = repo.getOneCommit(trueLink[1])
        issue = mysqlOperator.selectOneIssue(trueLink[2])
        comments = mysqlOperator.selectCommentInOneIssue(trueLink[2])
        diffs = repo.getOneDiff(commit)
        diffCodeList = []
        for diff in diffs:
            diffCode = preprocessor.processDiffCode(diff.diff)
            preDiffCode = preprocessor.processPreDiffCode(diff.diff)
            diffCodeList.append((codeModel.infer_vector(diffCode), codeModel.infer_vector(preDiffCode)))

        # code part init
        codeMax = -1
        temp['commitCode'] = []
        temp['issueCode'] = []
        # text part init
        commitText = preprocessor.preprocessToWord(commit.message.decode('utf-8'))
        commitTextVec = textModel.infer_vector(commitText)
        temp['commitText'] = commitTextVec  # 确定不变
        titleWords = preprocessor.preprocessToWord(issue[4].decode('utf-8'))
        temp['issueText'] = textModel.infer_vector(titleWords)  # 可能改变
        textMax = similarity(commitTextVec, temp['issueText'])
        # issue body
        if issue[5]:
            body = preprocessor.processHTML(issue[5].decode('utf-8'))
            bodyTextVec = textModel.infer_vector(body[1])
            sim = similarity(commitTextVec, bodyTextVec)
            if sim > textMax:
                temp['issueText'] = bodyTextVec
                textMax = sim
            if len(body[0]) > 0:
                codeVec = codeModel.infer_vector(body[0])
                for diffCodeTemp in diffCodeList:
                    codeSim = similarity(codeVec, diffCodeTemp[0])
                    if codeSim > codeMax:
                        temp['commitCode'] = diffCodeTemp[0]
                        temp['issueCode'] = codeVec
                        codeMax = codeSim
                    preCodeSim = similarity(codeVec, diffCodeTemp[1])
                    if preCodeSim > codeMax:
                        temp['commitCode'] = diffCodeTemp[1]
                        temp['issueCode'] = codeVec
                        codeMax = preCodeSim
        # issue comments
        for comment in comments:
            temp = preprocessor.processHTML(comment[4].decode('utf-8'))
            bodyTextVec = textModel.infer_vector(temp[1])
            sim = similarity(commitTextVec, bodyTextVec)
            if sim > textMax:
                temp['issueText'] = bodyTextVec
                textMax = sim
            if len(temp[0]) > 0:
                cCodeVec = codeModel.infer_vector(temp[0])
                for diffCodeTemp in diffCodeList:
                    codeSim = similarity(cCodeVec, diffCodeTemp[0])
                    if codeSim > codeMax:
                        temp['commitCode'] = diffCodeTemp[0]
                        temp['issueCode'] = cCodeVec
                        codeMax = codeSim
                    preCodeSim = similarity(cCodeVec, diffCodeTemp[1])
                    if preCodeSim > codeMax:
                        temp['commitCode'] = diffCodeTemp[1]
                        temp['issueCode'] = cCodeVec
                        codeMax = preCodeSim
        linkList.append(tempMap)

    for falseLink in falseLinkList:
        tempMap = {}
        temp['type'] = 0
        repo = repoMap[falseLink[0]]
        commit = repo.getOneCommit(falseLink[1])
        issue = mysqlOperator.selectOneIssue(falseLink[2])
        comments = mysqlOperator.selectCommentInOneIssue(falseLink[2])
        diffs = repo.getOneDiff(commit)
        diffCodeList = []
        for diff in diffs:
            diffCode = preprocessor.processDiffCode(diff.diff)
            preDiffCode = preprocessor.processPreDiffCode(diff.diff)
            diffCodeList.append((codeModel.infer_vector(diffCode), codeModel.infer_vector(preDiffCode)))

        # code part init
        codeMax = -1
        temp['commitCode'] = []
        temp['issueCode'] = []
        # text part init
        commitText = preprocessor.preprocessToWord(commit.message.decode('utf-8'))
        commitTextVec = textModel.infer_vector(commitText)
        temp['commitText'] = commitTextVec  # 确定不变
        titleWords = preprocessor.preprocessToWord(issue[4].decode('utf-8'))
        temp['issueText'] = textModel.infer_vector(titleWords)  # 可能改变
        textMax = similarity(commitTextVec, temp['issueText'])
        # issue body
        if issue[5]:
            body = preprocessor.processHTML(issue[5].decode('utf-8'))
            bodyTextVec = textModel.infer_vector(body[1])
            sim = similarity(commitTextVec, bodyTextVec)
            if sim > textMax:
                temp['issueText'] = bodyTextVec
                textMax = sim
            if len(body[0]) > 0:
                codeVec = codeModel.infer_vector(body[0])
                for diffCodeTemp in diffCodeList:
                    codeSim = similarity(codeVec, diffCodeTemp[0])
                    if codeSim > codeMax:
                        temp['commitCode'] = diffCodeTemp[0]
                        temp['issueCode'] = codeVec
                        codeMax = codeSim
                    preCodeSim = similarity(codeVec, diffCodeTemp[1])
                    if preCodeSim > codeMax:
                        temp['commitCode'] = diffCodeTemp[1]
                        temp['issueCode'] = codeVec
                        codeMax = preCodeSim
        # issue comments
        for comment in comments:
            temp = preprocessor.processHTML(comment[4].decode('utf-8'))
            bodyTextVec = textModel.infer_vector(temp[1])
            sim = similarity(commitTextVec, bodyTextVec)
            if sim > textMax:
                temp['issueText'] = bodyTextVec
                textMax = sim
            if len(temp[0]) > 0:
                cCodeVec = codeModel.infer_vector(temp[0])
                for diffCodeTemp in diffCodeList:
                    codeSim = similarity(cCodeVec, diffCodeTemp[0])
                    if codeSim > codeMax:
                        temp['commitCode'] = diffCodeTemp[0]
                        temp['issueCode'] = cCodeVec
                        codeMax = codeSim
                    preCodeSim = similarity(cCodeVec, diffCodeTemp[1])
                    if preCodeSim > codeMax:
                        temp['commitCode'] = diffCodeTemp[1]
                        temp['issueCode'] = cCodeVec
                        codeMax = preCodeSim
        linkList.append(tempMap)

    index += 1
    res = json.dumps(linkList, encoding="utf-8", indent=4)
    trainSet = open('./train/traincase%d.dat' % index, "w")
    trainSet.write(res)
    trainSet.close()
    print './train/traincase%d.dat' % index, 'Over'

    trueStart += TRUE_GAP
    falseStart += FALSE_GAP
    trueLinkList = linkOperator.selectInScope(('sql_true_link', trueStart, trueStart + TRUE_GAP))
    falseLinkList = linkOperator.selectInScope(('sql_false_link', falseStart, falseStart + FALSE_GAP))
mysqlOperator.close()
linkOperator.close()
