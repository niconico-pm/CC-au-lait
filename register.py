# -*- coding: utf-8 -*-
from urlparse import parse_qs
from lib import auth
import content

def redirect(environ, start_response, response_header=None):
    status = '301 Redirect'
    response_headers = [('Location', 'http://' + environ['HTTP_HOST'])]
    if response_header != None:
        response_headers += response_header
    start_response(status, response_headers)
    return []

def get_register(environ, start_response, message=''):
    status = '200 OK'
    response_headers = [('Content-type', 'text/html')]
    
    template = content.get_template("main.tpl")
    header = content.get_html("header.html")
    body = content.get_template("register.tpl").substitute(message=message)
    html = template.substitute(header=header, body=body)
    start_response(status, response_headers)
    return [html]

def post_register(environ, start_response):
    post = parse_qs(environ['wsgi.input'].read())
    if 'username' in post and 'password' in post and 'verifypassword' in post:
        username = post['username'][0]
        password = post['password'][0]
        verifypassword = post['verifypassword'][0]
        if password == verifypassword:
            if auth.find_passhash(username) == None:
                if auth.register_user(username, password):
                    passhash = auth.find_passhash(username)
                    header = auth.make_cookie(username, passhash)
                    return redirect(environ, start_response, header)
                else:
                    return get_register(environ, start_response, "ユーザーの登録に失敗しました")
            else:
                return get_register(environ, start_response, "Usernameが既に使われています")
        else:
            return get_register(environ, start_response, "2つのPasswordが一致しません")
    else:
        return get_register(environ, start_response, "UsernameとPasswordを入力してください。")

def application(environ, start_response):
    method = environ['REQUEST_METHOD']
    if method == 'GET':
        return get_register(environ, start_response)
    elif method == 'POST':
        return post_register(environ, start_response)
