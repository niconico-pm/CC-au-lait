# -*- coding: utf-8 -*-
from lib.middleware import Selector
from lib.auth import Authenticator
from lib import content
import common, login, register, setting, upload, mypage

table = dict()

def index(environ, start_response):
    template = content.get_template("main.tpl")
    body = content.get_html("index.html")
    header = common.header_html(environ)
    html = template.substitute(header=header, body=body)
    status = '200 OK'
    response_header = [('Content-type', 'text/html')]
    start_response(status, response_header)
    return [html]

table['/'] = index
table['/login'] = login.application
table['/logout'] = login.logout
table['/register'] = register.application
table['/setting'] = setting.application
table['/upload'] = upload.application
table['/mypage'] = mypage.application

application = Authenticator(Selector(table))
