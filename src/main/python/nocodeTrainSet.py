# -*- coding: UTF-8 -*-

from database import linkOperator, mysqlOperator
from gitresolver import gitResolver
import json
import sys
import random

reload(sys)
sys.setdefaultencoding('utf-8')


def getRandomFalse(falseTable, start, end, size):
    links = linkOperator.selectInScope((falseTable, start, end))
    return random.sample(links, size)


def buildTrainSet(trueTable, falseTable, repoId, repoPath, trueGap, falseGap, trueCount, falseCount):
    trueStart = 1
    falseStart = 1
    trueLinkList = linkOperator.selectInScope((trueTable, trueStart, trueStart + trueCount))
    falseLinkList = getRandomFalse(falseTable, falseStart, falseStart + falseGap, falseCount)

    index = 0
    repo = gitResolver.GitResolver(repoPath)
    while len(trueLinkList) > 0 and len(falseLinkList) > 0:
        print 'true: ', trueStart, ' to ', trueStart + trueCount
        print 'false: ', falseStart, ' to ', falseStart + falseCount
        linkList = []
        for trueLink in trueLinkList:
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
        trainSet = open('./train/traincase%d-%d.dat' % (repoId, index), "w")
        trainSet.write(res)
        trainSet.close()
        print './train/traincase%d-%d.dat' % (repoId, index), 'Over'

        trueStart += trueGap
        falseStart += falseGap
        trueLinkList = linkOperator.selectInScope((trueTable, trueStart, trueStart + trueCount))
        falseLinkList = getRandomFalse(falseTable, falseStart, falseStart + falseGap, falseCount)
    mysqlOperator.close()
    linkOperator.close()


if __name__ == '__main__':
    # buildTrainSet('true_link_nocode', 'false_link_nocode', 50904245, '/home/fdse/user/rh/gitrepo/apache/beam',
    #               510, 70000, 510, 600)
    # buildTrainSet('true_link_27729926', 'false_link_27729926', 27729926, '/home/fdse/user/rh/gitrepo/grpc-java',
    #               320, 16000, 320, 320)
    # buildTrainSet('true_link_13421878', 'false_link_13421878', 13421878, '/home/fdse/user/rh/gitrepo/pentaho-kettle',
    #               320, 19000, 320, 320)
    # buildTrainSet('true_link_12499251', 'false_link_12499251', 12499251, '/home/fdse/user/rh/gitrepo/checkstyle',
    #               320, 18000, 320, 320)
    buildTrainSet('true_link_20587599', 'false_link_20587599', 20587599, '/home/fdse/user/rh/gitrepo/flink',
                  320, 30000, 320, 320)

# FALSE_TABLE = 'heal_false_link'
# TRUE_TABLE = 'heal_true_link'
#
# repoMap = {}
# repoMap[50904245L] = gitResolver.GitResolver('/home/fdse/user/rh/gitrepo/apache/beam')
#
# TRUE_GAP = 510
# FALSE_GAP = 70000
# TRUE_COUNT = 510
# FALSE_COUNT = 600
