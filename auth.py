# -*- coding: utf-8 -*-
from Cookie import SimpleCookie
from hashlib import sha512

correct_username = "admin"
password_salt = "salt"
correct_passhash = sha512("pass" + password_salt).hexdigest()

def hash_password(password, salt):
    return sha512(password + salt).hexdigest()

def find_salt(username):
    if username == correct_username:
        return password_salt
    return None

def find_passhash(username):
    if username == correct_username:
        return correct_passhash
    return None

def validate(username, passhash):
    cor_passhash = find_passhash(username)
    if cor_passhash != None:
        return passhash == cor_passhash
    else:
        return False

def read_cookie(http_cookie):
    ck = SimpleCookie(http_cookie)
    if 'username' in ck and 'passhash' in ck:
        return (ck['username'].value, ck['passhash'].value)
    else:
        return None

def validate_cookie(environ):
    if 'HTTP_COOKIE' in environ:
        http_cookie = environ['HTTP_COOKIE']
        tup = read_cookie(http_cookie)
        if tup != None:
            return validate(*tup)
    return False

def make_cookie(username, passhash, expires):
    ckname_user = 'username'
    ckname_hash = 'passhash'
    
    ck = SimpleCookie()
    ck[ckname_user] = username
    ck[ckname_hash] = passhash
    if expires != None:
        ck[ckname_user]['expires'] = expires
        ck[ckname_hash]['expires'] = expires
    outlist = [
        ('Set-Cookie', ck[ckname_user].OutputString()),
        ('Set-Cookie', ck[ckname_hash].OutputString()),
    ]
    return outlist

def delete_cookie():
    return make_cookie_outputlist("deleted", "deleted", 0);

