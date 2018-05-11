# -*- coding: UTF-8 -*-

from database import linkOperator, mysqlOperatorCopy
from gitresolver import gitResolver
import re
import traceback

pattern = re.compile(r'https://api.github.com/repos/([\s\S]*?)/commits/.*', re.I)


def getPath(s):
    temp = re.sub(r'https://github.com/', '', s, 0, re.I)
    return "/home/fdse/data/prior_repository/" + temp


def getIssueInDate(cou):
    issues = mysqlOperatorCopy.selectAllIssueInOneRepoDate(cou)
    comments = mysqlOperatorCopy.selectAllCommentInOneRepoDate(cou)
    issueSet = []
    for issue in issues:
        if issue[1] not in issueSet:
            issueSet.append(issue[1])
    for comment in comments:
        if comment[1] not in issueSet:
            issueSet.append(comment[1])
    return issueSet


projects = linkOperator.selectRepoOver(5000)
print 'start'
for repo in projects:
    try:
        gitRepo = gitResolver.GitResolver(getPath(repo[1]))
        commits = gitRepo.getCommits()
        print '==============', getPath(repo[1]), 'Start'
        for commit in commits:
            commitSha = str(commit.hexsha.encode("utf-8"))
            print commitSha
            commitIssues = mysqlOperatorCopy.selectExistIssueOnCommit((repo[0], commitSha))
            trueLinks = []
            for ci in commitIssues:
                trueLinks.append(ci[2])
            issueByDate = getIssueInDate((repo[0], str(gitRepo.getDateTime(commit)), str(gitRepo.getDateTime(commit))))
            for i in issueByDate:
                if len(commitIssues) > 0:
                    if i in trueLinks:
                        linkOperator.insertLink(('sql_true_link', repo[0], commitSha, i))
                    else:
                        linkOperator.insertLink(('sql_false_link', repo[0], commitSha, i))
                else:
                    linkOperator.insertLink(('sql_unknow_link', repo[0], commitSha, i))
        print '==============', getPath(repo[1]), 'End'
    except Exception, e:
        print 'Error:', getPath(repo[1])
        print traceback.format_exc()
print 'end'
linkOperator.close()
mysqlOperatorCopy.close()
