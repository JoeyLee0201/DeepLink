# -*- coding: UTF-8 -*-

from database import linkOperator, mysqlOperator
from gitresolver import gitResolver
import re
import traceback

pattern = re.compile(r'https://api.github.com/repos/([\s\S]*?)/commits/.*', re.I)


def getPath(s):
    temp = re.sub(r'https://github.com/', '', s, 0, re.I)
    return "/home/fdse/data/prior_repository/" + temp


def getDiffday(date1, date2):
    return abs((date1 - date2).days)


def isUnlabeled(issue, date):
    if getDiffday(date, issue[2]) <= 7:
        return True
    if issue[3]:
        if getDiffday(date, issue[3]) <= 7:
            return True
    return False


# projects = linkOperator.selectRepoOver(5000)
projects = linkOperator.selectOneRepo(50904245)
print 'start'
for repo in projects:
    try:
        gitRepo = gitResolver.GitResolver(getPath(repo[1]))
        issues = mysqlOperator.selectAllIssueInOneRepo(repo[0])
        commits = gitRepo.getCommits()
        # repoName = re.sub(r'https://github.com/', '', repo[1], 0, re.I)
        print '==============', getPath(repo[1]), 'Start'
        for commit in commits:
            commitSha = str(commit.hexsha.encode("utf-8"))
            print commitSha
            commitIssues = mysqlOperator.selectExistIssueOnCommit((repo[0], commitSha))
            trueLinks = []
            for ci in commitIssues:
                if ci[0] in trueLinks:
                    pass
                else:
                    trueLinks.append(ci[0])
                    linkOperator.insertLink(('nocode_true_link', repo[0], commitSha, ci[0]))
            for issue in issues:
                if isUnlabeled(issue, gitRepo.getDateTime(commit)):
                    if len(commitIssues) > 0:
                        if issue[1] in trueLinks:
                            pass
                        else:
                            linkOperator.insertLink(('nocode_false_link', repo[0], commitSha, issue[1]))
                    else:
                        pass
        print '==============', getPath(repo[1]), 'End'
    except Exception, e:
        print 'Error:', getPath(repo[1])
        print traceback.format_exc()
print 'end'
linkOperator.close()
mysqlOperator.close()
