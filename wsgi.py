from lib.selector import Selector
import login
import content

def testpage(environ, start_response):
    start_response('200 OK', [('Content-type', 'text/plain')])
    return ["test page"]

def index(environ, start_response):
    template = content.get_template("index.tpl")
    header = content.get_html("header.html")

    status = '200 OK'
    response_header = [('Content-type', 'text/html')]
    start_response(status, response_header)
    return [template.substitute(header=header)]
    
application = Selector({
        '/test'  : testpage,
        '/login' : login.application,
        '/': index,
})
