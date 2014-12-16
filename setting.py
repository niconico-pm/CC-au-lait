# -*- coding: utf-8 -*-
from lib import auth, content, db
import common

def get_handler(environ, start_response, message=""):
    main_tpl = content.get_template("main.tpl")
    header = common.header_html(environ)
    tpl = content.get_template("setting.tpl")
    username = auth.Authenticator.get_username(environ)
    body = tpl.substitute(message=message, username=username, nickname="hoge", comment="none", ispublic="checked")
    html = main_tpl.substitute(header=header, body=body)
    status = '200 OK'
    response_headers = [('Content-type', 'text/html')]
    start_response(status, response_headers)
    return [html]

def post_handler(environ, start_response):
    return get_handler(environ, start_response)

def application(environ, start_response):
    method = environ.get('REQUEST_METHOD', 'GET')
    if method == 'GET':
        if auth.Authenticator.authenticated(environ):
            return get_handler(environ, start_response)
        else:
            return common.notice_error(environ, start_response, "ログインしてください")
    elif method == 'POST':
        return post_handler(environ, start_response)
