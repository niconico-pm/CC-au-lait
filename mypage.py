# -*- coding: utf-8 -*-
from lib import auth, content, db
from lib.score import ScoreGetter
import common

medallabel = ['FAILED', 'CLEAR', 'FC', 'P']
gradelabel = ['D', 'C', 'B', 'A', 'AA', 'AAA']
def get_grade(score):
    if   score >= 950000: return 5
    elif score >= 850000: return 4
    elif score >= 700000: return 3
    elif score >= 600000: return 2
    elif score >= 500000: return 1
    else                : return 0

def td(cont):
    return '<td>' + cont + '</td>'

class Getter(ScoreGetter):
    def init_scoredata(self):
        self.scoredata = self.get_scoredata()

    def make_totaltable(self):
        table = ""
        scoredata = self.scoredata
        musicnum = 0
        playednum = [0] * 4
        grade = [[0] * 7, [0] * 7, [0] * 7, [0] * 7]
        medal = [[0] * 5, [0] * 5, [0] * 5, [0] * 5]
        score = [0L] * 4
        for data in scoredata:
            _, scores = data
            musicnum += 1
            if len(scores) > 0:
                for dif, (scr, mdl, _) in enumerate(scores):
                    if scr is None:
                        grd = mdl = -1
                        scr = 0
                    else:
                        grd = get_grade(scr)
                        playednum[dif] += 1
                        playednum[3] += 1
                    grade[dif][grd] += 1
                    medal[dif][mdl] += 1
                    score[dif] += scr
                    grade[3][grd] += 1
                    medal[3][mdl] += 1
                    score[3] += scr
            else:
                for dif in range(3):
                    grade[dif][-1] += 1
                    medal[dif][-1] += 1
                    grade[3][-1] += 1
                    medal[3][-1] += 1
        mygradelabel = list(gradelabel)
        mygradelabel.reverse()
        mygradelabel += ['no play']
        for i, grdlbl in enumerate(mygradelabel):
            grd = 5 - i
            table += '<tr>'
            if i == 0: table += '<td rowspan="7">Grade</td>'
            table += td(grdlbl)
            for dif in range(4):
                table += td(str(grade[dif][grd]) + '/' + (str(musicnum) if dif != 3 else str(musicnum * 3)))
            table += '</tr>'
        mymedallabel = list(medallabel)
        mymedallabel.reverse()
        mymedallabel += ['no play']
        for i, mdllbl in enumerate(mymedallabel):
            mdl = 3 - i
            table += '<tr>'
            if i == 0: table += '<td rowspan="5">Medal</td>'
            table += td(mdllbl)
            for dif in range(4):
                table += td(str(medal[dif][mdl]) + '/' + (str(musicnum) if dif != 3 else str(musicnum * 3)))
            table += '</tr>'
        table += '<tr>'
        table += '<td rowspan="3">score</td>'
        table += td('合計スコア')
        for dif in range(4):
            table += td(str(score[dif]))
        table += '</tr>'
        table += '<tr>'
        table += td('プレイ済み平均')
        for dif in range(4):
            if playednum[dif] != 0:
                table += td(str(score[dif]/playednum[dif]))
            else:
                table += td('0')
        table += '</tr>'
        table += '<tr>'
        table += td('全曲平均')
        for dif in range(4):
            table += td(str(score[dif]/(musicnum if dif != 3 else musicnum * 3)))
        table += '</tr>'
        return table

    def make_scoretable(self):
        table = ""
        scoredata = self.scoredata
        for data in scoredata:
            table += "<tr>"
            music, scores = data
            table += '<td class="music-title">' + music[1].encode('utf-8') + "</td>"
            if len(scores) > 0:
                for scr, mdl, lvl in scores:
                    table += '<td>' + (str(scr) if not scr is None else "no play") + '</td>'
                    table += '<td>' + (medallabel[mdl] if not mdl is None else "") + '</td>'
                    table += '<td>' + (gradelabel[get_grade(scr)] if not scr is None else "") + '</td>'
                    table += '<td>' + (str(lvl) if not lvl is None else "") + '</td>'
            else:
                table += "<td colspan=12 align=center>--- No Data ---</td>"
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
    name = nickname.encode('utf-8') if nickname else username
    count = get_count(environ)
    getter = Getter(username)
    if getter.set_count(count):
        getter.init_scoredata()
        link = make_link(count, getter.maxcount)
        date = str(getter.get_date())
        totaltable = getter.make_totaltable()
        scoretable = getter.make_scoretable()
    else:
        link = ""
        date = ""
        totaltable = "<p>データがありません。</p>"
        scoretable = "<p>データがありません。</p>"
    getter.close()
    body = tpl.substitute(locals())
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
