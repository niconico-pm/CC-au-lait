# -*- coding: utf-8 -*-
from cgi import parse_qs
from Cookie import SimpleCookie
from hashlib import md5

correct_username = "admin"
correct_password = "pass"

def find_password(username):
    if username == correct_username:
        return correct_password
    else:
        return None

def hash_password(password):
    return md5(password).hexdigest()

def find_passhash(username):
    password = find_password(username)
    if password != None:
        return hash_password(password)
    return None

def validate(username, passhash):
    password = find_password(username)
    if password != None:
        return (passhash == hash_password(password))
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

def make_cookie_outputlist(username, passhash, expires):
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

def make_delete_cookie():
    return make_cookie_outputlist("deleted", "deleted", 0);

def application(environ, start_response):
    htmllogin = """\
<html>
<head>
<title>Login Page</title>
</head>
<body>
<h2>Login</h2>
<form method="POST" action="">
  %s
  <label for="username">Username:</label>
  <input type="text" name="username"><br>
  <label for="password">Password:</label>
  <input type="password" name="password"><br>
  <input type="submit" value="Login">
</form>
</body>
</html>
"""
    htmllogined = """\
<html><head>
<title>Login Succeed</title>
</head>
<body>
<h2>Login Succeed!</h2>
<p>Hello, %s!</p>
<form method="POST" action="">
  <input type="hidden" name="logout" value="1">
  <input type="submit" value="Logout">
</form>
</body>
</html>
"""
    status = '200 OK'
    response_headers = [('Content-type', 'text/html')]
    html = "init"

    method = environ['REQUEST_METHOD']
    if method == 'POST':
        post = parse_qs(environ['wsgi.input'].read())
        if 'username' in post and 'password' in post:
            username = post['username'][0]
            password = post['password'][0]
            passhash = hash_password(password)
            if validate(username, passhash):
                response_headers += make_cookie_outputlist(username, passhash, None)
                html = htmllogined % username
            else:
                html = htmllogin % ("Invalid Username or Passowrd" + "<br>")
        elif 'logout' in post:
            response_headers += make_delete_cookie()
            html = htmllogin % "Logouted.<br>"
        else:
            html = htmllogin % "Enter Username or Password<br>"
    elif 'HTTP_COOKIE' in environ:
        tup = read_cookie(environ['HTTP_COOKIE'])
        if tup != None:
            username, passhash = tup
            if validate(username, passhash):
                html = htmllogined % username
            else:
                html = htmllogin % ("Authrization failed (" + username + ", " + passhash + ")<br>")
        else:
            html = htmllogin % ("Invalid Cookie<br>")
    else:
        html = htmllogin % ""

    start_response(status, response_headers)
    return [html]
