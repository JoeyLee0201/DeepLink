# -*- coding: UTF-8 -*-

from database import linkOperator, mysqlOperator

projects = mysqlOperator.selectAllHighRepository()
print 'start'
for repo in projects:
    issues = mysqlOperator.selectAllIssueInOneRepo(repo[0])
    issueLen = len(issues)
    linkLen = 0
    for issue in issues:
        links = mysqlOperator.selectTrueLinkInOneIssue(issue[1])
        linkLen = linkLen + len(links)
    turple = (repo[0],repo[1],issueLen,linkLen)
    print turple,'\n'
    linkOperator.insertOneRepo(turple)
print 'end'
linkOperator.close()
mysqlOperator.close()