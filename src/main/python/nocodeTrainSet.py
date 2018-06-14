# -*- coding: UTF-8 -*-

from database import linkOperator, mysqlOperator
from gensim.models.doc2vec import Doc2Vec
from preprocessor import preprocessor
from gitresolver import gitResolver
import re
import traceback
import json
import sys
import random

reload(sys)
sys.setdefaultencoding('utf-8')

FALSE_TABLE = 'heal_false_link'
TRUE_TABLE = 'heal_true_link'

repoMap = {}
repoMap[50904245L] = gitResolver.GitResolver('/home/fdse/user/rh/gitrepo/apache/beam')

TRUE_GAP = 510
FALSE_GAP = 70000
TRUE_COUNT = 510
FALSE_COUNT = 600

trueStart = 1
falseStart = 1


def getRandomFalse(start, end, size):
    links = linkOperator.selectInScope((FALSE_TABLE, start, end))
    return random.sample(links, size)


trueLinkList = linkOperator.selectInScope((TRUE_TABLE, trueStart, trueStart+TRUE_COUNT))
falseLinkList = getRandomFalse(falseStart, falseStart + FALSE_GAP, FALSE_COUNT)


index = 0
while len(trueLinkList) > 0 and len(falseLinkList) > 0:
    print 'true: ', trueStart, ' to ', trueStart+TRUE_COUNT
    print 'false: ', falseStart, ' to ', falseStart+FALSE_COUNT
    linkList = []
    for trueLink in trueLinkList:
        repo = repoMap[trueLink[0]]
        commit = repo.getOneCommit(trueLink[1])
        issue = mysqlOperator.selectOneIssue(trueLink[2])
        if issue is None:
            continue

        res = {}
        res['type'] = 1
        res['commit'] = commit.message.decode('utf-8')
        res['issuetitle'] = issue[4].decode('utf-8')
        # issue body
        if issue[5]:
            res['issue'] = issue[5].decode('utf-8')
        else:
            res['issue'] = ''
        linkList.append(res)

    for falseLink in falseLinkList:
        repo = repoMap[falseLink[0]]
        commit = repo.getOneCommit(falseLink[1])
        issue = mysqlOperator.selectOneIssue(falseLink[2])
        if issue is None:
            continue

        res = {}
        res['type'] = 0
        res['commit'] = commit.message.decode('utf-8')
        res['issuetitle'] = issue[4].decode('utf-8')
        # issue body
        if issue[5]:
            res['issue'] = issue[5].decode('utf-8')
        else:
            res['issue'] = ''
        linkList.append(res)

    index += 1
    res = json.dumps(linkList, encoding="utf-8", indent=4)
    trainSet = open('./train/traincase%d.dat' % index, "w")
    trainSet.write(res)
    trainSet.close()
    print './train/traincase%d.dat' % index, 'Over'

    trueStart += TRUE_GAP
    falseStart += FALSE_GAP
    trueLinkList = linkOperator.selectInScope((TRUE_TABLE, trueStart, trueStart + TRUE_COUNT))
    falseLinkList = getRandomFalse(falseStart, falseStart + FALSE_GAP, FALSE_COUNT)
mysqlOperator.close()
linkOperator.close()
