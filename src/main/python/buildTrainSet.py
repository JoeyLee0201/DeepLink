# -*- coding: UTF-8 -*-

from database import linkOperator, mysqlOperator
from gensim.models.doc2vec import Doc2Vec
from preprocessor import preprocessor
from gitresolver import gitResolver
import re
import traceback


def getPath(s):
    temp = re.sub(r'https://github.com/', '', s, 0, re.I)
    return "/home/fdse/data/prior_repository/" + temp


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
textModel = Doc2Vec.load("text.model")
codeModel = Doc2Vec.load("code.model")

trueLinkList = linkOperator.selectInScope(('true_link', trueStart, trueStart+TRUE_GAP))
falseLinkList = linkOperator.selectInScope(('false_link', falseStart, falseStart+FALSE_GAP))

while len(trueLinkList) > 0 and len(falseLinkList) > 0:
    for trueLink in trueLinkList:
        repo = repoMap[trueLink[0]]
        commit = repo.getOneCommit(trueLink[1])
        # every true link
        commitText = preprocessor.preprocessToWord(commit.message.decode('utf-8'))
        diffs = repo.getOneDiff(commit)
        commitCode = []
        for diff in diffs:
            diffCode = preprocessor.processDiffCode(diff.diff)
            commitCode.extend(diffCode)
        issue = mysqlOperator.selectOneIssue(trueLink[2])
        comments = mysqlOperator.selectCommentInOneIssue(trueLink[2])
        titleWords = preprocessor.preprocessToWord(issue[4].decode('utf-8'))
        if issue[5]:
            body = preprocessor.processHTML(issue[5].decode('utf-8'))
            bodyWords = body[1]
            codeWords = body[0]
        for comment in comments:
            temp = preprocessor.processHTML(comment[4].decode('utf-8'))
            cBodyWords = temp[1]
            cCodeWords = temp[0]
    for falseLink in falseLinkList:
        # every false link
        pass
    trueStart += TRUE_GAP
    falseStart += FALSE_GAP
    trueLinkList = linkOperator.selectInScope(('true_link', trueStart, trueStart + TRUE_GAP))
    falseLinkList = linkOperator.selectInScope(('false_link', falseStart, falseStart + FALSE_GAP))
