# -*- coding: utf-8 -*-
from urlparse import parse_qs
from string import Template
from lib import auth
import content

def redirect(environ, start_response, response_header=None):
    status = '301 Redirect'
    response_headers = [('Location', 'http://' + environ['HTTP_HOST'])]
    if response_header != None:
        response_headers += response_header
    start_response(status, response_headers)
    return []

def get_login(environ, start_response, message=''):
    status = '200 OK'
    response_headers = [('Content-type', 'text/html')]
    
    template = content.get_template("main.tpl")
    header = content.get_html("header.html")
    body = content.get_template("login.tpl").substitute(message=message)
    html = template.substitute(header=header, body=body)
    start_response(status, response_headers)
    return [html]

def post_login(environ, start_response):
    post = parse_qs(environ['wsgi.input'].read())
    if 'username' in post and 'password' in post:
        username = post['username'][0]
        password = post['password'][0]
        if auth.validate_pass(username, password):
            passhash = auth.find_passhash(username)
            header = auth.make_cookie(username, passhash)
            return redirect(environ, start_response, header)
        else:
            return get_login(environ, start_response, "UsernameかPasswordが間違っています。")
    else:
        return get_login(environ, start_response, "UsernameとPasswordを入力してください。")

def logout(environ, start_response):
    tpl = content.get_template("main.tpl")
    header = content.get_html("header.html")
    html = tpl.substitute(header=header, body="<div>ログアウトしました。</div>")
    cookie = auth.delete_cookie()
    status = '200 OK'
    response_headers = [('Content-type', 'text/html')]
    response_headers += cookie
    start_response(status, response_headers)
    return [html]
    
def application(environ, start_response):
    method = environ['REQUEST_METHOD']
    if method == 'GET':
        if auth.validate_cookie(environ):
            return redirect(environ, start_response)
        else:
            return get_login(environ, start_response)
    elif method == 'POST':
        return post_login(environ, start_response)
