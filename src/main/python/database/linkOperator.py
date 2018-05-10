# -*- coding: UTF-8 -*-

import MySQLdb

con = MySQLdb.connect(host='10.131.252.160', port=3306, db='rhlink', user='root', passwd='root', charset='utf8')

cursor = con.cursor()   

def insertOneRepo(repo):
    SQL = """
    INSERT INTO `repo` (`repo_id`, `url`, `issues`, `true_links`) VALUES ('%d', '%s', '%d', '%d');
    """ % repo
    try:
        cursor.execute(SQL)
        con.commit()
    except Exception,e:
        print e
        con.rollback()

def insertLink(link):
    SQL = """
    INSERT INTO `%s` (`repo_id`, `sha`, `issue_index`) VALUES ('%d', '%s', '%s');
    """ % link
    try:
        cursor.execute(SQL)
        con.commit()
    except Exception,e:
        print e
        con.rollback()

def selectRepoOver(num):
    SQL = """
    select repo_id,url from repo where true_links > %d
    """
    try:
        cursor.execute(SQL % num)
        results = cursor.fetchall()
        return results
    except Exception,e:
        print e

def close():
    cursor.close()
    con.close()  


if __name__ == '__main__':
    # selectApichangeById(10)
    # selectApichangeByRepositoryAndType(-5, 'CHANGE_METHOD')
    # insertOneRepo((-1,'test',0,0))
    print selectRepoOver(5000)
    # insertLink(('true_link',-1,'test','test'))
    # insertLink(('false_link',-1,'test','test'))
    # insertLink(('unknow_link',-1,'test','test'))
    close()
