# -*- coding: utf-8 -*-
import sys, os
basedir = os.path.dirname(os.path.abspath(__file__))
#sys.path.append(basedir)
os.chdir(basedir)

from lib.middleware import Selector, StaticResponser, FileResponser
import app

application = Selector({
        '/css' : StaticResponser('html/css', 'text/css'),
        '/js' : StaticResponser('html/js', 'application/javascript'),
        '/image' : StaticResponser('html/image', 'image/png'),
        '/favicon.ico': FileResponser('html/favicon.ico', 'image/x-icon'),
        '': app.application,
        })
