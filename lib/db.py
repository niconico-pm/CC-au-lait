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

def register_user(username, passhash, salt):
    sql = "insert into " + TBL_User + \
        "(UserName, PassHash, PassSalt) values(" + \
        "'" + username + "', '" + passhash + "', '" + salt + "')"
    try:
        runsql(sql)
        return True
    except:
        return False

def get_column(keyname, key, column, table):
    sql = "select " + column + " from " + table + \
        " where " + keyname + " = '" + key + "'"
    try:
        res = runsql(sql)
    except:
        return None
    return res

def get_from_user(username, column):
    sql = "select " + column + " from " + TBL_User + \
        " where Username = '" + username + "'"
    try:
        res = runsql(sql)
    except Exception as inst:
        # とりあえずそのまんま投げる
        raise inst

    if(len(res) == 0):
        return None
    elif(len(res) == 1):
        return res[0][0].encode('utf-8')
    else:
        raise Exception("Double registration")

def get_passhash(username):
    return get_from_user(username, "PassHash")

def get_salt(username):
    return get_from_user(username, "PassSalt")
