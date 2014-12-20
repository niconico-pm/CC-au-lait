# -*- coding: utf-8 -*-
from Cookie import SimpleCookie
from hashlib import sha512
from uuid import uuid4
import db

def hash_password(password, salt):
    return sha512(password + salt).hexdigest()

def make_salt():
    return uuid4().hex

def find_salt(username):
    user = db.User.select(UserName = username).one()
    if user != None:
        return user.PassSalt

def find_passhash(username):
    user = db.User.select(UserName = username).one()
    if user != None:
        return user.PassHash

def user_exists(username):
    return db.User.select(UserName = username).one() != None

def register_user(username, password):
    salt = make_salt()
    passhash = hash_password(password, salt)
    return db.User.new(UserName = username, PassHash = passhash, PassSalt = salt) != None

def validate(username, passhash):
    cor_passhash = find_passhash(username)
    if cor_passhash != None:
        return passhash == cor_passhash
    else:
        return False

def validate_pass(username, password):
    salt = find_salt(username)
    if salt != None:
        passhash = hash_password(password, salt)
        return validate(username, passhash)
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

def make_cookie(username, passhash, expires=None):
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
    return make_cookie("deleted", "deleted", "Thu, 01-Jan-1970 00:00:01 GMT");

class Authenticator(object):
    ek_auth = 'Authenticated'
    ek_user = 'UserName'
    def __init__(self, application):
        self.application = application
    def __call__(self, environ, start_response):
        if validate_cookie(environ):
            username, _ = read_cookie(environ['HTTP_COOKIE'])
            environ[self.ek_auth] = True
            environ[self.ek_user] = username
        return self.application(environ, start_response)

    @classmethod
    def authenticated(cls, environ):
        return environ.get(cls.ek_auth, False)

    @classmethod
    def get_username(cls, environ):
        return environ.get(cls.ek_user, '')
