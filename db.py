# -*- coding: utf-8 -*-
import MySQLdb

MySQL_Host = "localhost"
MySQL_User = "httpd"
MySQL_PassWd = "Password"
MySQL_Charset = "utf8"
MySQL_DB = "BST_ScoreTool"

TBL_User = "user"
TBL_Music = "music"
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

def regist_user(username, passhash, salt):
    try:
        runsql("insert into " + TBL_User + " values(" + 
               username + ", " + passhash + ", " + salt + ")")
        return True
    except:
        return False

def get_column(keyname, key, column, table):
    try:
        res = runsql("select " + column + " from " + table +
                     "where " + keyname + " = " + key):
        return res
    except:
        return None

    
def get_from_user(username, column):
    res = runsql("select " + column + " from " + TBL_User +
                 "where Username = " + username)
    if(len(res) == 1):
        return res[0]
    else:
        return None

def get_passhash(username):
    return get_from_user(username, "PassHash")

def get_salt(username):
    return get_from_user(username, "PassSalt")
