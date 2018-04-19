# -*- coding: UTF-8 -*-

import MySQLdb

con = MySQLdb.connect(host='localhost', port=3306, db='apichangeast', user='root', passwd='123456', charset='utf8')

cursor = con.cursor()    #创建一个游标对象

def selectApichangeById(id):
    SQL = """
    select * from apichange where apichange_id = %d
    """
    try:
        cursor.execute(SQL % id)
        res = cursor.fetchone()
        while res:
          print res
          res = cursor.fetchone()    #fetchone只给出一条数据，然后游标后移。游标移动过最后一行数据后再fetch就得到None
    except Exception,e:
        print e
        con.rollback()

def selectApichangeByRepositoryAndType(id, type):
    SQL = """
    select * from apichange where repository_id = %s and change_type = %s
    """
    try:
        cursor.execute(SQL, (id, type))
        res = cursor.fetchone()
        while res:
          print res
          res = cursor.fetchone()    #fetchone只给出一条数据，然后游标后移。游标移动过最后一行数据后再fetch就得到None
    except Exception,e:
        print e
        con.rollback()

def close():
    cursor.close()
    con.close()  


if __name__ == '__main__':
    selectApichangeById(10)
    selectApichangeByRepositoryAndType(-5, 'CHANGE_METHOD')
    close()