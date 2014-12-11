# -*- coding: utf-8 -*-
from urlparse import parse_qs
from string import Template
from mylib import auth

htmllogin = Template("""\
<html>
<head>
<title>Login Page</title>
</head>
<body>
<h2>Login</h2>
<form method="POST" action="">
  ${message}<br>
  <label for="username">Username:</label>
  <input type="text" name="username"><br>
  <label for="password">Password:</label>
  <input type="password" name="password"><br>
  <input type="submit" value="Login">
</form>
</body>
</html>
""")
htmllogined = Template("""\
<html><head>
<title>Login Succeed</title>
</head>
<body>
<h2>Login Succeed!</h2>
<p>Hello, ${username}!</p>
<form method="POST" action="">
  <input type="hidden" name="logout" value="1">
  <input type="submit" value="Logout">
</form>
</body>
</html>
""")

def application(environ, start_response):
    status = '200 OK'
    response_headers = [('Content-type', 'text/html')]
    html = "init"

    method = environ['REQUEST_METHOD']
    if method == 'POST':
        post = parse_qs(environ['wsgi.input'].read())
        if 'username' in post and 'password' in post:
            username = post['username'][0]
            password = post['password'][0]
            salt = auth.find_salt(username)
            if salt != None:
                passhash = auth.hash_password(password, salt)
                if auth.validate(username, passhash):
                    response_headers += auth.make_cookie(username, passhash)
                    html = htmllogined.substitute(username=username)
                else:
                    html = htmllogin.substitute(message="Wrong password.")
            else:
                html = htmllogin.substitute(message="Not registered: " + username)
        elif 'logout' in post:
            response_headers += auth.delete_cookie()
            html = htmllogin.substitute(message="Logouted.")
        else:
            html = htmllogin.substitute(message="Enter Username or Password")
    elif 'HTTP_COOKIE' in environ:
        tup = auth.read_cookie(environ['HTTP_COOKIE'])
        if tup != None:
            username, passhash = tup
            if auth.validate(username, passhash):
                html = htmllogined % username
            else:
                html = htmllogin.substitute(message="Authrization failed (" + username + ", " + passhash + ")")
        else:
            html = htmllogin.substitute(message="Invalid Cookie")
    else:
        html = htmllogin.substitute(message="")

    start_response(status, response_headers)
    return [html]
