# -*- coding: utf-8 -*-
from lib.middleware import Selector
from lib.auth import Authenticator
from lib import content
import common, login, register, setting

table = dict()
def addtable(path):
    def decorator(app):
        table[path] = app
        return app
    return decorator

def regular_page(htmlgen):
    def application(environ, start_response):
        html = htmlgen(environ)
        status = '200 OK'
        response_header = [('Content-type', 'text/html')]
        start_response(status, response_header)
        return [html]
    return application

@addtable('/')
@regular_page
def index(environ):
    template = content.get_template("main.tpl")
    body = content.get_html("index.html")
    header = common.header_html(environ)
    return template.substitute(header=header, body=body)

table['/login'] = login.application
table['/logout'] = login.logout
table['/register'] = register.application
table['/setting'] = setting.application

application = Authenticator(Selector(table))
