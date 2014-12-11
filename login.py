# -*- coding: utf-8 -*-
from urlparse import parse_qs
from string import Template
from lib import auth
import content

def redirect(environ, start_response):
    status = '301 Redirect'
    response_header = [('Location', 'http://' + environ['HTTP_HOST'])]
    start_response(status, response_header)
    return []

def get_login(environ, start_response, message=''):
    status = '200 OK'
    response_headers = [('Content-type', 'text/html')]
    template = content.get_template("login.tpl")
    header = content.get_html("header.html")
    html = template.substitute(header=header, message=message)
    start_response(status, response_headers)
    return [html]

def post_login(environ, start_response):
    post = parse_qs(environ['wsgi.input'].read())
    if 'username' in post and 'password' in post:
        username = post['username'][0]
        password = post['password'][0]
        if auth.validate_pass(username, password):
            passhash = auth.find_passhash(username)
            response_headers = auth.make_cookie(username, passhash)
            status = '301 Redirect'
            response_headers += [('Location', 'http://' + environ['HTTP_HOST'])]
            start_response(status, response_headers)
            return []
        else:
            return get_login(environ, start_response, "UsernameかPasswordが間違っています。")
    else:
        return get_login(environ, start_response, "UsernameとPasswordを入力してください。")

def application(environ, start_response):
    method = environ['REQUEST_METHOD']
    if method == 'GET':
        if auth.validate_cookie(environ):
            return redirect(environ, start_response)
        else:
            return get_login(environ, start_response)
    elif method == 'POST':
        return post_login(environ, start_response)
