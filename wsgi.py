from lib.selector import Selector
from lib import auth
import login, register
import content

def testpage(environ, start_response):
    start_response('200 OK', [('Content-type', 'text/plain')])
    return ["test page"]

def index(environ, start_response):
    template = content.get_template("main.tpl")
    body = content.get_html("index.html")
    if auth.validate_cookie(environ):
        header_tpl = content.get_template("header_loggedin.tpl")
        username, _ = auth.read_cookie(environ['HTTP_COOKIE'])
        header = header_tpl.substitute(username=username)
    else:
        header = content.get_html("header.html")

    html = template.substitute(header=header, body=body)
    status = '200 OK'
    response_header = [('Content-type', 'text/html')]
    start_response(status, response_header)
    return [html]

application = Selector({
        '/test'  : testpage,
        '/login' : login.application,
        '/logout': login.logout,
        '/register' : register.application,
        '/': index,
        })
