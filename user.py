# -*- coding: utf-8 -*-
from lib import auth, content, db
from lib.score import ScoreGetter
import common, mypage

def get_username_and_count(environ):
    pathinfo = environ['PATH_INFO']
    try:
        s = pathinfo.find('/', 1)
        username = None
        if s > 0:
            username = pathinfo[1:s]
            count = int(pathinfo[s + 1:])
        else:
            username = pathinfo[1:]
            count = -1
    except ValueError:
        count = -1
    finally:
        return username, count

def make_link(count, maxcount, username):
    prev = count - 1
    next = count + 1
    prevlink = '<a href="/user/' + username + '/%d" style="float: left">< 前の更新</a>' % prev
    nextlink = '<a href="/user/' + username + '/%d" style="float: right">次の更新 ></a>' % next
    return (prevlink if count != 0 and count != - (maxcount + 1) else "") +\
           (nextlink if count != maxcount and next != 0 else "")

def get_handler(environ, start_response):
    main_tpl = content.get_template("main.tpl")
    header = common.header_html(environ)
    tpl = content.get_template("mypage.tpl")
    username, count = get_username_and_count(environ)
    if username:
        user = db.User.select(UserName=username).one()
        if user:
            if user.IsPublic:
                nickname = user.NickName
                name = nickname.encode('utf-8') if nickname else username
                getter = mypage.Getter(username)
                if getter.set_count(count):
                    link = make_link(count, getter.maxcount, username)
                    date = str(getter.get_date())
                    table = getter.make_table()
                else:
                    link = ""
                    date = ""
                    table = "<p>スコアデータがありません。</p>"
                getter.close()
                body = tpl.substitute(locals())
            else:
                body = "<h3>ユーザーがスコアデータを非公開にしています。</h3>"
        else:
            body = "<h3>ユーザーが存在しません。</h3>"
    else:
        body = "<h3>ユーザ指定が不正です。</h3>"
    html = main_tpl.substitute(header=header, body=body)
    status = '200 OK'
    response_headers = [('Content-type', 'text/html')]
    start_response(status, response_headers)
    return [html]

def application(environ, start_response):
    return get_handler(environ, start_response)
