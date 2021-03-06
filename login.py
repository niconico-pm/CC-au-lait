# -*- coding: utf-8 -*-
from urlparse import parse_qs
from lib import auth, content, middleware
import common

def get_handler(environ, start_response, message=''):    
    template = content.get_template("main.tpl")
    header = common.header_html(environ)
    body = content.get_template("login.tpl").substitute(message=message)
    html = template.substitute(header=header, body=body)

    status = '200 OK'
    response_headers = [('Content-type', 'text/html')]
    start_response(status, response_headers)
    return [html]

def post_handler(environ, start_response):
    post = parse_qs(environ['wsgi.input'].read())
    if 'username' in post and 'password' in post:
        username = post['username'][0]
        password = post['password'][0]
        if auth.validate_pass(username, password):
            passhash = auth.find_passhash(username)
            header = auth.make_cookie(username, passhash)
            return common.redirect_top(environ, start_response, header)
        else:
            return get_handler(environ, start_response, "UsernameかPasswordが間違っています。")
    else:
        return get_handler(environ, start_response, "UsernameとPasswordを入力してください。")

def logout(environ, start_response):
    if not auth.Authenticator.authenticated(environ):
        return common.redirect_top(environ, start_response)
    tpl = content.get_template("main.tpl")
    environ.pop('Authenticated')
    header = common.header_html(environ)
    html = tpl.substitute(header=header, body="<h3>ログアウトしました。</h3>")
    cookie = auth.delete_cookie()
    status = '200 OK'
    response_headers = [('Content-type', 'text/html')]
    response_headers += cookie
    start_response(status, response_headers)
    return [html]

def application(environ, start_response):
    method = environ.get('REQUEST_METHOD', 'GET')
    if method == 'GET':
        if auth.Authenticator.authenticated(environ):
            return common.redirect_top(environ, start_response)
        else:
            return get_handler(environ, start_response)
    elif method == 'POST':
        return post_handler(environ, start_response)
    
