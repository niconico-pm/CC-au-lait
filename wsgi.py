from selector import Selector
import login
import os

def testpage(environ, start_response):
    start_response('200 OK', [('Content-type', 'text/plain')])
    return ["test page"]

def index(environ, start_response):
    status = '200 OK'
    response_header = [('Content-type', 'text/html')]
    start_response(status, response_header)
    return """\
<html>
<head>
<meta charset="UTF-8">
<title>CC-au-lait TestPage</title>
</head>
<body>
<div>
<h2>Welcome to CC-au-lait Test Page</h2>
</div>
<hr>
<div>
<a href="login">login page</a><br>
</div>
</body>
</html>
"""

application = Selector({
        '/test'  : testpage,
        '/login' : login.application,
        '/': index,
})
