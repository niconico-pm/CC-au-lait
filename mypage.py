# -*- coding: utf-8 -*-
from lib import auth, content, db
from lib.score import ScoreGetter
import common

medal = ['fail', 'Clear', 'F.C.', 'P']

def make_table(username):
    getter = ScoreGetter()
    scoredata = getter.get_scoredata(username)
    getter.close()
    table = ""
    for data in scoredata:
        table += "<tr>"
        music, scores = data
        table += '<td>'
        table += music[1].encode('utf-8')
        table += "</td>"
        if len(scores) > 0:
            for dif in range(0, 3):
                table += '<td align=center>'
                if scores[dif][0]:
                    table += str(scores[dif][0])
                else:
                    table += "no play"
                table += "</td>"
                table += '<td align=center>'
                if scores[dif][1]:
                    table += medal[scores[dif][1]]
                else:
                    table += " "
                table += "</td>"
        else:
            table += "<td colspan=6 align=center>!No Data!</td>"
        table += "</tr>"
    return table
def get_handler(environ, start_response):
    main_tpl = content.get_template("main.tpl")
    header = common.header_html(environ)
    tpl = content.get_template("mypage.tpl")
    username = auth.Authenticator.get_username(environ)
    table = make_table(username)
    body = tpl.substitute(username=username, table=table)
    html = main_tpl.substitute(header=header, body=body)
    status = '200 OK'
    response_headers = [('Content-type', 'text/html')]
    start_response(status, response_headers)
    return [html]

def application(environ, start_response):
    if auth.Authenticator.authenticated(environ):
        return get_handler(environ, start_response)
    else:
        return common.notice_error(environ, start_response, "ログインしてください")
