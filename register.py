# -*- coding: utf-8 -*-
from urlparse import parse_qs
from lib import auth, content
import common

def get_handler(environ, start_response, message=''):
    status = '200 OK'
    response_headers = [('Content-type', 'text/html')]
    
    template = content.get_template("main.tpl")
    header = content.get_html("header.html")
    body = content.get_template("register.tpl").substitute(message=message)
    html = template.substitute(header=header, body=body)
    start_response(status, response_headers)
    return [html]

def post_handler(environ, start_response):
    post = parse_qs(environ['wsgi.input'].read())
    if 'username' in post and 'password' in post and 'verifypassword' in post:
        username = post['username'][0]
        password = post['password'][0]
        verifypassword = post['verifypassword'][0]
        if password == verifypassword:
            if not auth.user_exists(username):
                if auth.register_user(username, password):
                    passhash = auth.find_passhash(username)
                    header = auth.make_cookie(username, passhash)
                    return common.redirect_top(environ, start_response, header)
                else:
                    return get_handler(environ, start_response, "ユーザーの登録に失敗しました")
            else:
                return get_handler(environ, start_response, "Usernameが既に使われています")
        else:
            return get_handler(environ, start_response, "2つのPasswordが一致しません")
    else:
        return get_handler(environ, start_response, "UsernameとPasswordを入力してください。")

def notice_logout(environ, start_response):
    tpl = content.get_template("main.tpl")
    username, _ = auth.read_cookie(environ['HTTP_COOKIE'])
    header = content.get_template("header_loggedin.tpl").substitute(username=username)
    html = tpl.substitute(header=header, body="<h3>ログアウトしてください</h3>")
    status = '200 OK'
    response_headers = [('Content-type','text/html')]
    start_response(status, response_headers)
    return [html]

def application(environ, start_response):
    method = environ['REQUEST_METHOD']
    if method == 'GET':
        if auth.validate_cookie(environ):
            return notice_logout(environ, start_response)
        else:
            return get_handler(environ, start_response)
    elif method == 'POST':
        return post_handler(environ, start_response)
