# -*- coding: utf-8 -*-
from lib.middleware import Selector
from lib.auth import Authenticator
import index, login, register

table = dict()
table['/'] = index.application
table['/login'] = login.application
table['/logout'] = login.logout
table['/register'] = register.application

application = Authenticator(Selector(table))
