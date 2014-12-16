# -*- coding: utf-8 -*-
from lib import auth, content

def redirect_top(environ, start_response, additional_headers=[]):
    status = '303 See Other'
    response_headers = [('Location', 'http://' + environ['HTTP_HOST'])]
    response_headers += additional_headers
    start_response(status, response_headers)
    return []

def notice_message(environ, start_response, message="エラーが発生しました"):
    tpl = content.main_template()
    header = content.get_html("header.html")
    html = tpl.substitute(header=header, body="<h3>ログアウトしました。</h3>")
    status = '200 OK'
    response_headers = [('Content-type', 'text/html')]
    start_response(status, response_headers)
    return [html]
