# -*- coding: utf-8 -*-
from lib import auth, content, db
from lib.score import ScoreGetter
import common

medal = ['FAILED', 'CLEAR', 'FC', 'P']
def grade(score):
    if   score >= 950000: return 'AAA'
    elif score >= 850000: return 'AA'
    elif score >= 700000: return 'A'
    elif score >= 600000: return 'B'
    elif score >= 500000: return 'C'
    else                : return 'D'

class Getter(ScoreGetter):
    def make_table(self):
        table = ""
        scoredata = self.get_scoredata()
        for data in scoredata:
            table += "<tr>"
            music, scores = data
            table += '<td class="music-title">' + music[1].encode('utf-8') + "</td>"
            if len(scores) > 0:
                for dif in range(0, 3):
                    table += '<td>' + (str(scores[dif][0]) if not scores[dif][0] is None else "no play") + '</td>'
                    table += '<td>' + (medal[scores[dif][1]] if not scores[dif][1] is None else "") + '</td>'
                    table += '<td>' + (grade(scores[dif][0]) if not scores[dif][0] is None else "") + '</td>'
            else:
                table += "<td colspan=9 align=center>! --- No Data --- !</td>"
            table += "</tr>\n"
        return table

def get_count(environ):
    pathinfo = environ['PATH_INFO']
    try:
        countstr = pathinfo[1:]
        count = int(countstr)
    except ValueError:
        count = -1
    finally:
        return count

def make_link(count, maxcount):
    prev = count - 1
    next = count + 1
    prevlink = '<a href="/mypage/%d" style="float: left">< 前の更新</a>' % prev
    nextlink = '<a href="/mypage/%d" style="float: right">次の更新 ></a>' % next
    return (prevlink if count != 0 and count != - (maxcount + 1) else "") +\
           (nextlink if count != maxcount and next != 0 else "")

def get_handler(environ, start_response):
    main_tpl = content.get_template("main.tpl")
    header = common.header_html(environ)
    tpl = content.get_template("mypage.tpl")
    username = auth.Authenticator.get_username(environ)
    nickname = db.User.select(UserName=username).one().NickName
    count = get_count(environ)
    getter = Getter(username)
    if getter.set_count(count):
        link = make_link(count, getter.maxcount)
        date = str(getter.get_date())
        table = getter.make_table()
    else:
        link = ""
        date = ""
        table = "<p>スコアデータがありません。</p>"
    getter.close()
    body = tpl.substitute(name=nickname.encode('utf-8') if nickname else username, link=link, date=date, table=table)
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
