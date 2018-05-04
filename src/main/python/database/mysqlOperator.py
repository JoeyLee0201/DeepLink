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
    select repository_id,issue_index,created_at,closed_at,title,body,labels,type from issue where repository_id = %d and type = 'issue'
    """
    try:
        cursor.execute(SQL % repoId)
        results = cursor.fetchall()
        return results
    except Exception,e:
        print e

def selectTrueLinkInOneIssue(issueIndex):
    SQL = """
    select repository_id,issue_index,created_at,commit_id from issue_event where issue_index = '%s' and commit_id is not null
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
    print selectCommentInOneIssue('JakeWharton/ActionBarSherlock/issues/3')
    close()