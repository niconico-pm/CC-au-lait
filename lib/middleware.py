# -*- coding: utf-8 -*-
from wsgiref import util
import os

def notFound(environ, start_response):
    start_response('404 NotFound', [('Content-type', 'text/html')])
    return ["<h1>Not found</h1><p>The requested url %s was not found.</p>" % util.request_uri(environ)]

class Selector(object):
    '''
    パスによるアプリケーション振り分けを行う
    '''
    def __init__(self, table, notfound=notFound):

        # パスは長い順にマッチさせたいので、あらかじめソートしておく
        tmp = sorted(table, key=lambda x:len(x), reverse=True)

        # 扱いやすいように、タプルのリストにしておく
        table = [(x, table[x]) for x in tmp]

        self.table = table

        # 割り振るパスが見つからなかったときに呼び出すアプリケーション
        self.notfound = notfound

    def __call__(self, environ, start_response):
        ''' リクエストのパスを見て振り分ける '''
        scriptname = environ.get('SCRIPT_NAME', '')
        pathinfo = environ.get('PATH_INFO', '')

        for p, app in self.table:
            if p == '' or p == '/' and pathinfo.startswith(p):
                return app(environ, start_response)

            # 同じパスならそのまま
            # 同じパスで始まっていて、その後にスラッシュがある
            if pathinfo == p or pathinfo.startswith(p) and pathinfo[len(p)] == '/':
                # リクエスト情報を書き換える
                util.shift_path_info(environ)
                return app(environ, start_response)

        return self.notfound(environ, start_response)

class StaticResponser(object):
    '''
    cssのような静的ファイルを返すmiddleware
    filedirの下を探してあったらmime_typeファイルとして返す、なかったらnotfound
    '''
    def __init__(self, filedir, mime_type, notfound=notFound):
        basedir = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..")
        self.path = os.path.join(basedir, filedir)
        self.notfound = notfound
        self.mime_type = mime_type

    def __call__(self, environ, start_response):
        # path_infoから最初の/を削る
        filename = environ['PATH_INFO'][1:]
        filepath = os.path.join(self.path, filename)
        try:
            content = open(filepath, 'r').read()
        except IOError:
            content = filepath
#            return self.notfound(environ, start_resnponse)

        status = '200 OK'
        response_headers = [('Content-type', self.mime_type),
                            ('Content-Length', str(len(content)))]
        start_response(status, response_headers)
        return [content]
