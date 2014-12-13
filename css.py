# -*- coding: utf-8 -*-
from lib import content    

def application(environ, start_response):
    # path_infoから最初の/を削る
    filename = environ['PATH_INFO'][1:]
    try:
        css = content.get_css(filename)
        status = '200 OK'
    except IOError:
        css = filename + ' was not found'
        status = '404 NotFound'

    response_headers = [('Content-type', 'text/css'),
                        ('Content-Length', str(len(css)))]
    start_response(status, response_headers)
    return [css]
