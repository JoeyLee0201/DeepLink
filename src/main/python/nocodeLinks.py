# -*- coding: UTF-8 -*-

from database import linkOperator, mysqlOperator
from gitresolver import gitResolver
import traceback
import nocodeRepoInfo


def getDiffday(date1, date2):
    return abs((date1 - date2).days)


def isUnlabeled(issue, date):
    if getDiffday(date, issue[2]) <= 7:
        return True
    if issue[3]:
        if getDiffday(date, issue[3]) <= 7:
            return True
    return False


def buildLinks(repoId):
    print 'start'
    try:
        repoPath = nocodeRepoInfo.REPO_MAP[nocodeRepoInfo.USE_REPO_INDEX]['path']
        gitRepo = gitResolver.GitResolver(repoPath)
        issues = mysqlOperator.selectAllIssueInOneRepo(repoId)
        commits = gitRepo.getCommits()
        # repoName = re.sub(r'https://github.com/', '', repo[1], 0, re.I)
        print '==============', repoPath, 'Start'
        for commit in commits:
            commitSha = str(commit.hexsha.encode("utf-8"))
            print commitSha
            commitIssues = mysqlOperator.selectExistIssueOnCommit((repoId, commitSha))
            trueLinks = []
            for ci in commitIssues:
                if ci[0] in trueLinks:
                    pass
                else:
                    trueLinks.append(ci[0])
                    linkOperator.insertLink(('true_link_%d' % repoId, repoId, commitSha, ci[0]))
            for issue in issues:
                if isUnlabeled(issue, gitRepo.getDateTime(commit)):
                    if len(commitIssues) > 0:
                        if issue[1] in trueLinks:
                            pass
                        else:
                            linkOperator.insertLink(('false_link_%d' % repoId, repoId, commitSha, issue[1]))
                    else:
                        pass
        print '==============', repoPath, 'End'
    except Exception, e:
        print 'Error:', repoPath
        print traceback.format_exc()
    print 'end'
    linkOperator.close()
    mysqlOperator.close()


if __name__ == '__main__':
    buildLinks(nocodeRepoInfo.REPO_MAP[nocodeRepoInfo.USE_REPO_INDEX]['id'])
