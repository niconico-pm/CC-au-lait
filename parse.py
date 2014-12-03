# -*- coding: utf-8 -*-

from HTMLParser import HTMLParser

class MyHTMLParser(HTMLParser):
    def __init__(self):
        self.nowtag = ''
        HTMLParser.__init__(self)

    def handle_data(self, data):
        if self.nowtag == 'title':
            print data

    def handle_starttag(self, tag, attr):
        self.nowtag = tag

    def handle_endtag(self, tag):
        if tag == self.nowtag:
            self.nowtag = ''

f = open('ronri.html', 'r')
allLines = f.read()
f.close()

parser = MyHTMLParser()
parser.feed(allLines)
