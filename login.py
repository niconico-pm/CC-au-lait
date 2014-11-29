# -*- coding: utf-8 -*-
from cgi import parse_qs
from Cookie import SimpleCookie
from hashlib import md5

correct_username = "admin"
correct_password = "pass"

htmllogin = """
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
htmllogined = """
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

def application(environ, start_response):
    global htmllogin
    global htmllogined

    status = '200 OK'
    response_headers = [('Content-type', 'text/html')]
    html = "init"

    method = environ['REQUEST_METHOD']
    post=parse_qs(environ['wsgi.input'].read())
    if method == 'POST':
        if 'logout' in post:
            ck = SimpleCookie()
            ck['username'] = "deleted"
            ck['username']['expires'] = 0
            ck['passhash'] = "deleted"
            ck['passhash']['expires'] = 0
            response_headers.append(('Set-Cookie', ck['username'].OutputString()))
            response_headers.append(('Set-Cookie', ck['passhash'].OutputString()))
            html = htmllogin % "Logouted.<br>"
        elif 'username' in post and 'password' in post:
            username = post['username'][0]
            password = post['password'][0]
            if username == correct_username and password == correct_password:
                ck = SimpleCookie()
                ck['username'] = username
                ck['passhash'] = md5(password).hexdigest()
                response_headers.append(('Set-Cookie', ck['username'].OutputString()))
                response_headers.append(('Set-Cookie', ck['passhash'].OutputString()))
                html = htmllogined % username
            else:
                html = htmllogin % "Invalid Username or Passowrd<br>"
        else:
            html = htmllogin % "Enter Username or Password<br>"
    elif 'HTTP_COOKIE' in environ:
        ck = SimpleCookie(environ['HTTP_COOKIE'])
        username = ck['username'].value
        passhash = ck['passhash'].value
        if username == correct_username and passhash == md5(correct_password).hexdigest():
            html = htmllogined % username
        else:
            html = htmllogin % ("Invalid Cookie<br>" + username + ", " + passhash)
    else:
        html = htmllogin % ""

    start_response(status, response_headers)
    return [html]
