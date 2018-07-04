# -*- coding: UTF-8 -*-

from database import linkOperator, mysqlOperator
from gitresolver import gitResolver
import json
import sys
import random
import nocodeRepoInfo

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
        trainSet = open('./train%d/traincase%d-%d.dat' % (repoId, repoId, index), "w")
        trainSet.write(res)
        trainSet.close()
        print './train%d/traincase%d-%d.dat' % (repoId, repoId, index), 'Over'

        trueStart += trueGap
        falseStart += falseGap
        trueLinkList = linkOperator.selectInScope((trueTable, trueStart, trueStart + trueCount))
        falseLinkList = getRandomFalse(falseTable, falseStart, falseStart + falseGap, falseCount)
    mysqlOperator.close()
    linkOperator.close()


if __name__ == '__main__':
    repo_id = nocodeRepoInfo.REPO_MAP[nocodeRepoInfo.USE_REPO_INDEX]['id']
    repo_path = nocodeRepoInfo.REPO_MAP[nocodeRepoInfo.USE_REPO_INDEX]['path']
    buildTrainSet('true_link_%d' % repo_id, 'false_link_%d' % repo_id, repo_id, repo_path,
                  nocodeRepoInfo.REPO_MAP[nocodeRepoInfo.USE_REPO_INDEX]['trueGap'],
                  nocodeRepoInfo.REPO_MAP[nocodeRepoInfo.USE_REPO_INDEX]['falseGap'],
                  nocodeRepoInfo.REPO_MAP[nocodeRepoInfo.USE_REPO_INDEX]['trueCount'],
                  nocodeRepoInfo.REPO_MAP[nocodeRepoInfo.USE_REPO_INDEX]['falseCount'])

