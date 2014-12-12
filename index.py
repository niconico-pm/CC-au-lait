from lib import auth, content

def application(environ, start_response):
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
