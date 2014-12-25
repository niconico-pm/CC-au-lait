# -*- coding: utf-8 -*-
from urlparse import parse_qs
from lib import auth, content, db
from lib.score import ScoreParser, ScoreUpdater
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
    username = environ['UserName']
    if 'scorehtml' in post:
        scorehtml = post['scorehtml'][0]
        updater = None
        try:
            parser = ScoreParser()
            parser.feed(scorehtml)
            scoredata = parser.get_scoredata()
            if len(scoredata) <= 0: raise
            updater = ScoreUpdater()
            updater.update_data(username, scoredata)
        except:
            if updater:
                updater.rollback()
            return get_handler(environ, start_response, "データの読み込みに失敗しました。申し訳ねえ。")
        else:
            updater.close()
            return common.redirect(environ, start_response, '/mypage')
    else:
        return get_handler(environ, start_response, message="ソースを入力してください。")

def application(environ, start_response):
    method = environ.get('REQUEST_METHOD', 'GET')
    if method == 'GET':
        if auth.Authenticator.authenticated(environ):
            return get_handler(environ, start_response)
        else:
            return common.notice_error(environ, start_response, "ログインしてください。")
    elif method == 'POST':
        return post_handler(environ, start_response)
