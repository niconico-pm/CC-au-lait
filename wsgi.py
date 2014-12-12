from lib.selector import Selector
import index, login, register

def testpage(environ, start_response):
    start_response('200 OK', [('Content-type', 'text/plain')])
    return ["test page"]

application = Selector({
        '/test'  : testpage,
        '/login' : login.application,
        '/logout': login.logout,
        '/register' : register.application,
        '/': index.application,
        })
