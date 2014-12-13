# -*- coding: utf-8 -*-
from lib.selector import Selector
import css, index, login, register

def test_env(environ, start_response):
    start_response('200 OK', [('Content-type', 'text/plain')])
    yield "scrip_name: " + environ['SCRIPT_NAME']
    yield "\npath_info: " + environ['PATH_INFO']
    
testpage = test_env

application = Selector({
        '/css'   : css.application,
        '/test'  : testpage,
        '/login' : login.application,
        '/logout': login.logout,
        '/register' : register.application,
        '/': index.application,
        })
