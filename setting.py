# -*- coding: utf-8 -*-
from urlparse import parse_qs
from lib import auth, content, db
import common

def get_handler(environ, start_response, message=""):
    main_tpl = content.get_template("main.tpl")
    header = common.header_html(environ)
    tpl = content.get_template("setting.tpl")
    username = auth.Authenticator.get_username(environ)
    user = db.User.select(UserName = username).one()
    body = tpl.substitute(
        message = message,
        username = username,
        nickname = user.NickName.encode('utf-8') if user.NickName else "",
        comment = user.Comment.encode('utf-8') if user.Comment else "",
        ispublic = "checked" if user.IsPublic else "",
        ) 
    html = main_tpl.substitute(header=header, body=body)
    status = '200 OK'
    response_headers = [('Content-type', 'text/html')]
    start_response(status, response_headers)
    return [html]

def post_handler(environ, start_response):
    post = parse_qs(environ['wsgi.input'].read())
    username = auth.Authenticator.get_username(environ)
    user = db.User.select(UserName = username).one()
    if 'nickname' in post:
        nickname = post['nickname'][0]
        user.update(NickName = nickname.decode('utf-8'))
    else:
        user.update(NickName = None)
    if 'comment' in post:
        comment = post['comment'][0]
        user.update(Comment = comment.decode('utf-8'))
    else:
        user.update(Comment = None)
    if 'ispublic' in post:
        user.update(IsPublic = True)
    else:
        user.update(IsPublic = False)
    return get_handler(environ, start_response, "設定が完了しました。")

def application(environ, start_response):
    method = environ.get('REQUEST_METHOD', 'GET')
    if method == 'GET':
        if auth.Authenticator.authenticated(environ):
            return get_handler(environ, start_response)
        else:
            return common.notice_error(environ, start_response, "ログインしてください。")
    elif method == 'POST':
        return post_handler(environ, start_response)
