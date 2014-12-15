# -*- coding: utf-8 -*-
from lib import auth, content

def notice_login(environ, start_response):
    tpl = content.get_template("main.tpl")
    header = content.get_html("header.html")
    body = "<h3>ログインしてください</h3>"
    html = tpl.substitute(header=header, body=body)
    status = '200 OK'
    response_headers = [('Content-type', 'text/html')]
    return [html]

def get_handler(environ, start_response):
    pass

def post_handler(environ, start_response):
    pass

def application(environ, start_response):
    pass
