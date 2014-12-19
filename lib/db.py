# -*- coding: utf-8 -*-
import MySQLdb

MySQL_Host = "localhost"
MySQL_User = "httpd"
MySQL_PassWd = "Password"
MySQL_Charset = "utf8"
MySQL_DB = "BST_ScoreTool"

TBL_User = "user"
TBL_Music = "music"
TBL_Updation = "updation"
TBL_Score = "score"

def get_connection():
    return MySQLdb.connect(
        host=MySQL_Host,
        db=MySQL_DB,
        user=MySQL_User,
        passwd=MySQL_PassWd,
        charset=MySQL_Charset)
common_connector = get_connection()

def commit():
    common_connector.commit()

# 削除予定
def runsql(sql):
    connector = get_connection()
    cursor = connector.cursor()
    cursor.execute(sql)
    result = cursor.fetchall()
    connector.commit()
    cursor.close()
    connector.close()
    return result

class Query(object):
    def __init__(self, cur, sql, vals):
        self.cur = cur
        self.sql = sql
        self.vals = vals
    def where(self, **kwargs):
        sql = self.sql
        vals = list(self.vals)
        k, v = kwargs.popitem()
        sql += " where " + k + " = %s"
        vals += [v]
        for k, v in kwargs.items():
            sql += " and " + k + " = %s"
            vals += [v]
        return Query(self.cur, sql, vals)
    def one(self):
        self.cur.execute(self.sql, self.vals)
        return self.cur.fetchone()
    def all(self):
        self.cur.execute(self.sql, self.vals)
        return self.cur.fetchall()

class Table(object):
    def __init__(self, table_name):
        self.cur = common_connector.cursor(MySQLdb.cursors.DictCursor)
        self.table_name = table_name
        sql = "select * from " + self.table_name
        self.query = Query(self.cur, sql, [])

class UserTable(Table):
    def __init__(self):
        Table.__init__(self, "user")

    def register(self, username, passhash, passsalt):
        sql = "insert into " + self.table_name + "(UserName, PassHash, PassSalt) values(%s, %s, %s)"
        vals = [username, passhash, passsalt]
        try:
            self.cur.execute(sql, vals)
        except:
            return False
        common_connector.commit()
        return True
user = UserTable()

class Column(object):
    def __init__(self, column_name):
        self.column_name = column_name
        
    def __get__(self, obj, kind):
        return self.value

    def __set__(self, obj, value):
        sql = "update " + obj.table.table_name + " set " + self.column_name + " = %s where " + obj.pk + " = %s"
        vals = (value, obj.__dict__[obj.pk])
        obj.table.cur.execute(sql, vals)
        

class Entity(object):
    # def __init__(self, **kwargs, insertflag=True):
    #     if insertflag:
    #         pass
    #     else:
    #         for k, v in kwargs.iteritems():
    #             self.__dict__[k].value = v;
        
class User(Entity):
    table = user
    UID = ("UID")
    UserName = ("UserName")
    NickName = ("NickName")
    Comment = ("Comment")
    IsPublic = ("IsPublic")
    PassHash = ("PassHash")
    PassSalt = ("PassSalt")
    pk = 'UID'
