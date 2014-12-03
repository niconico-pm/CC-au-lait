# import selecter

def testpage(environ, start_response):
    status = '200 OK'
    response_header = [('Content-type', 'text/plain')]
    start_response(status, response_header)

    return ["test page"]

application = testpage
