# -*- coding: utf-8 -*-
from urlparse import parse_qs
from lib import auth, content, db
from lib.parser import ScoreParser
import common

def get_handler(environ, start_response, message=""):
    main_tpl = content.get_template("main.tpl")
    header = common.header_html(environ)
    tpl = content.get_template("upload.tpl")
    username = auth.Authenticator.get_username(environ)
    body = tpl.substitute(message=message)
    html = main_tpl.substitute(header=header, body=body)
    status = '200 OK'
    response_headers = [('Content-type', 'text/html')]
    start_response(status, response_headers)
    return [html]

def post_handler(environ, start_response):
    post = parse_qs(environ['wsgi.input'].read())
    if 'scorehtml' in post:
        scorehtml = post['scorehtml'][0]
        parser = ScoreParser()
        parser.feed(scorehtml)
        scorelist = parser.get_scorelist()
        start_response('200 OK', [('Content-type', 'text/plain')])
        return [str(scorelist)]
    else:
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
