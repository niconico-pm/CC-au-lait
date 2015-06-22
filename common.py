# -*- coding: utf-8 -*-
from urllib import quote

from lib import auth, content

def header_html(environ):
    headertpl = content.get_template("header.tpl")
    urlbase = "http://" + environ['HTTP_HOST']
    if auth.Authenticator.authenticated(environ):
        username = auth.Authenticator.get_username(environ)
        menu = content.get_template("menu_loggedin.tpl").substitute(username=username)
        url = urlbase + "/user/" + quote(username)
        data_count = 'data-count="none" '
    else:
        menu = content.get_html("menu_loggedout.html")
        url = urlbase
        data_count = ""
    header = headertpl.substitute(locals())
    return header

def redirect(environ, start_response, location='/'):
    status = '303 See Other'
    response_headers = [('Location', 'http://' + environ['HTTP_HOST'] + location)]
    start_response(status, response_headers)
    return []    

def redirect_top(environ, start_response, additional_headers=[]):
    status = '303 See Other'
    response_headers = [('Location', 'http://' + environ['HTTP_HOST'])]
    response_headers += additional_headers
    start_response(status, response_headers)
    return []

def notice_error(environ, start_response, message="エラーが発生しました"):
    tpl = content.get_template("main.tpl")
    header = header_html(environ)
    html = tpl.substitute(header=header, body="<h3>%s</h3>"%message)
    status = '200 OK'
    response_headers = [('Content-type', 'text/html')]
    start_response(status, response_headers)
    return [html]
