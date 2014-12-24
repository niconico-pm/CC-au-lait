# -*- coding: utf-8 -*-

from HTMLParser import HTMLParser
import urllib2

class MyHTMLParser(HTMLParser):
    def __init__(self):
        self.nowtag = ''
        self.nowattr = ''
        self.musiclist = []
        self.music = [None] # ID
        self.level = [None] * 3 # Light, Medium, beast
        self.inmusicarea = False
        HTMLParser.__init__(self)

    def handle_data(self, data):
        if self.inmusicarea:
            for name, value in self.nowattr:
                if self.nowtag == 'img':
                    self.music = value.split('/')[-1].split('.')[0]
                if name == 'class':
                    if value == 'level_b':
                        self.level[0] = data
                    if value == 'level_n':
                        self.level[1] = data
                    if value == 'level_h':
                        self.level[2] = data

    def handle_starttag(self, tag, attr):
        self.nowtag = tag
        self.nowattr = attr
        if tag == 'ul':
            for name, value in attr:
                if name == 'class' and value == 'music_list':
                    self.inmusicarea = True


    def handle_endtag(self, tag):
        if self.inmusicarea:
            if tag == 'li':
                self.musiclist.append((self.music, tuple(self.level)))
            if tag == 'ul':
                self.inmusicarea = False

        if tag == self.nowtag:
            self.nowtag = ''
            self.nowattr = ''

    def get_musiclist(self):
        return self.musiclist

f = open('musiclist.html', 'r')
allLines = f.read()
f.close()

parser = MyHTMLParser()
parser.feed(allLines)

musiclist = parser.get_musiclist()
print musiclist

f = open('musiclist.csv', 'w')
for music in musiclist:
    f.write(str(music[0]) + ",0," + music[1][0] + "\n")
    f.write(str(music[0]) + ",1," + music[1][1] + "\n")
    f.write(str(music[0]) + ",2," + music[1][2] + "\n")
f.close()
