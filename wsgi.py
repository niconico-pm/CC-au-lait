# -*- coding: utf-8 -*-
from lib.middleware import Selector, StaticResponser
import app

application = Selector({
        '/css' : StaticResponser('html/css', 'text/css'),
        '': app.application,
        })
