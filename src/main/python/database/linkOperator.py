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


def selectOneRepo(id):
    SQL = """
    select repo_id,url from repo where repo_id = %d
    """
    try:
        cursor.execute(SQL % id)
        results = cursor.fetchall()
        return results
    except Exception, e:
        print e


def count(tableName):
    SQL = """
        select count(*) from %s
        """
    try:
        cursor.execute(SQL % tableName)
        results = cursor.fetchone()
        return results
    except Exception, e:
        print e


def selectInScope(cou):
    SQL = """
        select repo_id,sha,issue_index from %s where id >= %d and id < %d
        """
    try:
        cursor.execute(SQL % cou)
        results = cursor.fetchall()
        return results
    except Exception, e:
        print e


def insertCossim(cou):
    SQL = """
    INSERT INTO `cossim` (`type`, `cossim`) VALUES ('%d', '%f');
    """ % cou
    try:
        cursor.execute(SQL)
        con.commit()
    except Exception, e:
        print e
        con.rollback()


def close():
    cursor.close()
    con.close()  


if __name__ == '__main__':
    # selectApichangeById(10)
    # selectApichangeByRepositoryAndType(-5, 'CHANGE_METHOD')
    # insertOneRepo((-1,'test',0,0))
    # print selectRepoOver(5000)
    # insertLink(('true_link',-1,'test','test'))
    # insertLink(('false_link',-1,'test','test'))
    # insertLink(('unknow_link',-1,'test','test'))
    # print count('true_link')
    # print count('false_link')
    # print len(selectInScope(('true_link', 2500, 2600)))
    print selectOneRepo(12983151)
    close()
