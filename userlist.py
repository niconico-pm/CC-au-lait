# -*- coding: utf-8 -*-
from lib import content, db
import common

def td(data):
    return "<td>" + data + "</td>"

def make_userlist_table():
    con = db.SimpleConnection()
    cur = con.cur
    cur.execute("select UserName, NickName, Comment from user where IsPublic = 1 order by LastUpdate desc, UID");
    result = cur.fetchall()
    con.close()

    table = ""
    for username, nickname, comment in result:
        usernamestr = username.encode('utf-8')
        url = "/user/" + usernamestr
        table += "<tr>"
        table += td(nickname.encode('utf-8') if not nickname is None else usernamestr)
        table += td(comment.encode('utf-8') if not comment is None else "")
        table += td('<a href="' + url + '">' + url + '</a>')
        table += "</tr>"
    return table

def application(environ, start_response):
    template = content.get_template("main.tpl")
    tpl = content.get_template("userlist.tpl")
    tbody = make_userlist_table()
    body = tpl.substitute(locals())
    header = common.header_html(environ)
    html = template.substitute(header=header, body=body)
    status = '200 OK'
    response_header = [('Content-type', 'text/html')]
    start_response(status, response_header)
    return [html]
