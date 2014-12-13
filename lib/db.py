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

def runsql(sql):
    connector = MySQLdb.connect(
        host=MySQL_Host,
        db=MySQL_DB,
        user=MySQL_User,
        passwd=MySQL_PassWd,
        charset=MySQL_Charset)
    cursor = connector.cursor()
    cursor.execute(sql)
    result = cursor.fetchall()
    connector.commit()
    cursor.close()
    connector.close()
    return result

def quote(string):
    return "'" + string + "'"

def paren(string):
    return "(" + string + ")"

def comma(*args):
    return ", ".join(args)

def sqljoin(*args):
    return " ".join(args)

def sqlstr(arg):
    if type(arg) == str:
        return quote(arg)
    else:
        return str(arg)

def sqlvalues(*args):
    return comma(*[sqlstr(arg) for arg in args])

def select(column, table):
    return "select " + column + " from " + table

def where(keycol, key):
    return "where " + keycol + " = " + sqlstr(key)

def insert_into(table, columns, values):
    return "insert into " + table + paren(comma(*columns)) +\
        " values" + paren(sqlvalues(*values))

def register_user(username, passhash, passsalt):
    sql = insert_into(TBL_User, ('UserName', 'PassHash', 'PassSalt'), 
                      (username, passhash, passsalt))
    try:
        runsql(sql)
    except:
        return False
    return True

def get_from_user(username, column):
    sql = sqljoin(select(column, 'user'), where('Username', username))
    res = runsql(sql)
    if(len(res) == 0):
        return None
    elif(len(res) == 1):
        return res[0][0].encode('utf-8')
    else:
        raise Exception("Double registration")

def get_UID(username):
    return get_from_user(username, "UID")

def get_passhash(username):
    return get_from_user(username, "PassHash")

def get_salt(username):
    return get_from_user(username, "PassSalt")

