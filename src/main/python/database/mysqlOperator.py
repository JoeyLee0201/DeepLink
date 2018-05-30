# -*- coding: UTF-8 -*-

import MySQLdb

con = MySQLdb.connect(host='10.141.221.73', port=3306, db='codehub', user='root', passwd='root', charset='utf8')
# con = MySQLdb.connect(host='localhost', port=3306, db='apichangeast', user='root', passwd='123456', charset='utf8')

cursor = con.cursor()    #创建一个游标对象

# def selectApichangeById(id):
#     SQL = """
#     select * from apichange where apichange_id = %d
#     """
#     try:
#         cursor.execute(SQL % id)
#         res = cursor.fetchone()
#         while res:
#           print res
#           res = cursor.fetchone()    #fetchone只给出一条数据，然后游标后移。游标移动过最后一行数据后再fetch就得到None
#     except Exception,e:
#         print e

# def selectApichangeByRepositoryAndType(id, type):
#     SQL = """
#     select * from apichange where repository_id = %s and change_type = %s
#     """
#     try:
#         cursor.execute(SQL, (id, type))
#         res = cursor.fetchone()
#         while res:
#           print res
#           res = cursor.fetchone()    #fetchone只给出一条数据，然后游标后移。游标移动过最后一行数据后再fetch就得到None
#     except Exception,e:
#         print e

def selectAllHighRepository():
    SQL = """
    select repository_id, url from repository_high_quality
    """
    try:
        cursor.execute(SQL)
        results = cursor.fetchall()
        return results
    except Exception,e:
        print e

def selectAllIssueInOneRepo(repoId):
    SQL = """
    select repository_id,issue_index,created_at,closed_at,title,body,labels,type from issue where repository_id = %d
    """
    try:
        cursor.execute(SQL % repoId)
        results = cursor.fetchall()
        return results
    except Exception, e:
        print e

def selectOneIssue(issueIndex):
    SQL = """
    select repository_id,issue_index,created_at,closed_at,title,body,labels,type from issue where issue_index = '%s'
    """
    try:
        cursor.execute(SQL % issueIndex)
        results = cursor.fetchone()
        return results
    except Exception, e:
        print e

def selectTrueLinkInOneIssue(issueIndex):
    SQL = """
    select repository_id,issue_index,created_at,commit_id,commit_url from issue_event where issue_index = '%s' and commit_id is not null
    """
    try:
        cursor.execute(SQL % issueIndex)
        results = cursor.fetchall()
        return results
    except Exception,e:
        print e

def selectShaInOneIssue(issueIndex):
    SQL = """
    select commit_id from issue_event where issue_index = '%s' and commit_id is not null
    """
    try:
        cursor.execute(SQL % issueIndex)
        results = cursor.fetchall()
        return results
    except Exception,e:
        print e


def selectCommentInOneIssue(issueIndex):
    SQL = """
    select repository_id,issue_index,created_at,updated_at,body from issue_comment where issue_index = '%s'
    """
    try:
        cursor.execute(SQL % issueIndex)
        results = cursor.fetchall()
        return results
    except Exception,e:
        print e


def selectExistIssueOnCommit(cou):
    SQL = """
    select issue_index, repository_id, commit_id from issue_event where repository_id = %d and commit_id = '%s'
    """ % cou
    try:
        cursor.execute(SQL)
        results = cursor.fetchall()
        return results
    except Exception, e:
        print e


def countTrueLinkInOneIssue(issueIndex):
    SQL = """
    select count(event_id) from issue_event where issue_index = '%s' and commit_id is not null
    """
    try:
        cursor.execute(SQL % issueIndex)
        results = cursor.fetchone()
        return results
    except Exception,e:
        print e


# id, date, date
def selectAllIssueInOneRepoDate(cou):
    SQL = """
    select repository_id,issue_index from issue where repository_id = %d
    and (('%s' between DATE_SUB(created_at, INTERVAL 7 DAY) and DATE_ADD(created_at, INTERVAL 7 DAY)) 
    or ('%s' between DATE_SUB(closed_at, INTERVAL 7 DAY) and DATE_ADD(closed_at, INTERVAL 7 DAY)))
    """
    try:
        cursor.execute(SQL % cou)
        results = cursor.fetchall()
        return results
    except Exception, e:
        print e


# id, date, date
def selectAllCommentInOneRepoDate(cou):
    SQL = """
    select repository_id,issue_index from issue_comment where repository_id = %d 
    and (('%s' between DATE_SUB(created_at, INTERVAL 7 DAY) and DATE_ADD(created_at, INTERVAL 7 DAY)) 
    or ('%s' between DATE_SUB(updated_at, INTERVAL 7 DAY) and DATE_ADD(updated_at, INTERVAL 7 DAY)))
    """
    try:
        cursor.execute(SQL % cou)
        results = cursor.fetchall()
        return results
    except Exception, e:
        print e


def close():
    cursor.close()
    con.close()  


if __name__ == '__main__':
    # projects = selectAllHighRepository()
    # for repo in projects:
    #     issues = selectAllIssueInOneRepo(repo[0])

    #     for issue in issues:
    #         links = selectTrueLinkInOneIssue(issue[1])
    #         print len(links),'\n'
    # print len(selectAllIssueInOneRepo(1459486))
    # links = list(selectShaInOneIssue('JakeWharton/ActionBarSherlock/issues/3'))
    # trueLinks = []
    # for link in links:
    #     trueLinks.append(link[0])
    # print selectAllIssueInOneRepoDate((1451060, '2011-03-18 11:45:51', '2011-03-18 11:45:51'))
    # print len(selectOneIssue('checkstyle/checkstyle/issues/270'))
    # print selectExistIssueOnCommit((50904245, 'd56db36408aa9b45ea6d685d035c983c76a14b06'))
    print selectOneIssue('apache/beam/issues/2601')
    close()
