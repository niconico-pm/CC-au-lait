# -*- coding: utf-8 -*-

from HTMLParser import HTMLParser
import urllib2

class MyHTMLParser(HTMLParser):
    def __init__(self):
        self.nowtag = ''
        self.nowattr = ''
        self.scorelist = []
        self.score = [None] * 4
        self.scorearea_depth = 0
        self.inscorearea = False
        self.dif = 0
        HTMLParser.__init__(self)
        
    def handle_data(self, data):
        if self.nowtag == 'div' or self.nowtag == 'span':
            for name, value in self.nowattr:
                if name  == 'class':
                    if value == 'mymusic_tit':
                        self.score[0] = data 
                    if self.dif == 'light':
                        self.score[1] = data
                    if self.dif == 'medium':
                        self.score[2] = data
                    if self.dif == 'beast':
                        self.score[3] = data                                        

    def handle_starttag(self, tag, attr):
        self.nowtag = tag
        self.nowattr = attr
        if tag == 'div':
            if self.inscorearea:
                self.scorearea_depth += 1
                for name, value in attr:
                    if value == 'light':
                        self.dif = value
                    if value == 'medium':
                        self.dif = value
                    if value == 'beast':
                        self.dif = value
            else:
                for name, value in attr:
                    if name  == 'class' and value == 'score_area':
                        self.scorearea_depth = 1
                        self.dif = 1
                        self.inscorearea = True
                        self.score[1] = None                    
                        self.score[2] = None                    
                        self.score[3] = None

    def handle_endtag(self, tag):
        if tag == 'div':
            if self.inscorearea:
                self.scorearea_depth -= 1
                if self.scorearea_depth == 0:
                    self.scorelist.append(tuple(self.score))
                    self.inscorearea = False
        if tag == self.nowtag:
            self.nowtag = ''
            self.nowattr = ''

    def get_scorelist(self):
        return self.scorelist

f = open('beast_2.html', 'r')
allLines = f.read()
f.close()

parser = MyHTMLParser()
parser.feed(allLines)

scorelist = parser.get_scorelist()
print scorelist
for score in scorelist:
    print "曲名   :", score[0]
    print "Light  :", score[1]
    print "Medium :", score[2]
    print "Beast  :", score[3]
