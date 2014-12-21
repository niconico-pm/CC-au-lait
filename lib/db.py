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

def get_cursor(con):
    return con.cursor(MySQLdb.cursors.DictCursor)

common_cursor = get_cursor(common_connector)

def commit():
    common_connector.commit()

class Connection(object):
    def __init__(self):
        self.con = get_connection()
        self.cur = get_cursor(self.con)
    def commit(self):
        self.con.commit()
    def rollback(self):
        self.con.rollback()
    def close(self):
        self.cur.close()
        self.con.close()

class SimpleConnection(Connection):
    def __init__(self):
        self.con = get_connection()
        self.cur = self.con.cursor()

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
    def __init__(self, cls, sql, vals):
        self.cls = cls
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
        return Query(self.cls, sql, vals)

    def one(self):
        con = Connection()
        con.cur.execute(self.sql, self.vals)
        result = con.cur.fetchone()
        con.close()
        if result:
            entity = self.cls(**result)
            return entity

    def all(self):
        con = Connection()
        con.cur.execute(self.sql, self.vals)
        result = con.cur.fetchall()
        con.close()
        entities = [self.cls(**entity) for entity in result]
        return entities

class Column(object):
    def __init__(self, colum_name, entity):
        self.column_name = column_name
        self.entity = entity    # parent entity
        self._value = None

    def get_value(self):
        return self._value

class Entity(object):
    '''
    Entityのための抽象クラス
    __init__はEntityを作るだけで
    classmethodのnewでDBにinsertが発行される
    '''
    def __init__(self, **kwargs):
        for column in self.columns:
            self.__dict__[column] = None
        for column, value in kwargs.iteritems():
            self.__dict__[column] = value
        for pk_column in self.pk:
            pk_value = self.__dict__.get(pk_column, None)
            if pk_value == None:
                raise Exception("Primary Key should not be NULL")

    @classmethod
    def new(cls, **kwargs):
        sql = "insert into " + cls.table_name + "("
        columns = []
        vals = []
        for k, v in kwargs.iteritems():
            columns += [k]
            vals += [v]
        sql += ", ".join(columns)
        sql += ") values(" + ", ".join(["%s"] * len(vals)) + ")"
        try:
            con = Connection()
            con.cur.execute(sql, vals)
            entity = cls.select(**kwargs).one()
        except:
            con.rollback()
            entity = None
        else:
            con.commit()
            con.close()
        return entity

    @classmethod
    def select(cls, **kwargs):
        sql = "select * from " + cls.table_name
        vals = []
        if len(kwargs) > 0:
            k, v = kwargs.popitem()
            sql += " where " + k + " = %s"
            vals += [v]
            for k, v in kwargs.items():
                sql += " and " + k + " = %s"
                vals += [v]
        return Query(cls, sql, vals)

    def update(self, **kwargs):
        vals = []
        data = []
        for k, v in kwargs.iteritems():
            data += [k + " = %s"]
            vals += [v]
        pk = []
        for k in self.pk:
            pk += [k + " = %s"]
            vals += [self.__dict__[k]]
        sql = "update " + self.table_name + " set " + ", ".join(data) +  " where " + " and ".join(pk)
        try:
            con = Connection()
            con.cur.execute(sql, vals)
        except:
            con.rollback()
            con.close()
            return False
        else:
            con.commit()
            con.close()
            for k, v in kwargs.iteritems():
                self.__dict__[k] = v
            return True
    def __repr__(self):
        return str(self.__class__) + " object " + str(self.__dict__)

class User(Entity):
    table_name = 'user'
    columns = ("UID", "UserName", "NickName", "Comment", "IsPublic", "PassHash", "PassSalt")
    pk = ("UID",)

class Music(Entity):
    table_name = 'music'
    columns = ("MusicID", "Name")
    pk = ("Name",)

class Updation(Entity):
    table_name = 'updation'
    columns = ("Count", "UID", "Date")
    pk = ("Count", "UID")

class Score(Entity):
    table_name = 'score'
    columns = ("UID", "MusicID", "Difficulty", "UpCount", "Score", "Medal")
    pk = ("UID", "MusicID", "Difficulty", "UpCount")
