# -*- coding: utf-8 -*-

from HTMLParser import HTMLParser
import urllib2

class MyHTMLParser(HTMLParser):
    def __init__(self):
        self.nowtag = ''
        self.nowattr = ''
        self.scorelist = []
        self.score = [None] * 7
        self.difarea_depth = 0
        self.inscorearea = False
        self.dif = 0
        HTMLParser.__init__(self)

    def handle_data(self, data):
        if self.nowtag == 'div' or self.nowtag == 'span' or self.nowtag == 'img':
            for name, value in self.nowattr:
                if name == 'class':
                    if value == 'mymusic_tit':
                        self.score[0] = data
                    else:
                        for i in range(1,4):
                            if self.dif == i:
                                if value == 'score_num':
                                    self.score[(2 * i) - 1] = data
                                if value == 'perfect':
                                    self.score[2 * i] = 'Perfect'
                                if value == 'fullcombo':
                                    self.score[2 * i] = 'FullCombo'
                                if value == 'clear':
                                    self.score[2 * i] = 'Clear'
                                if value == 'failed':
                                    self.score[2 * i] = 'Failed'
                                if value == 'grade':
                                    self.dif = 0
    
    def handle_starttag(self, tag, attr):
        self.nowtag = tag
        self.nowattr = attr
        if tag == 'div':
            if self.inscorearea:
                self.scorearea_depth += 1
                for name, value in attr:
                    if value == 'light':
                        self.dif = 1
                    if value == 'medium':
                        self.dif = 2
                    if value == 'beast':
                        self.dif = 3

            else:
                for name, value in attr:
                    if name == 'class' and value == 'score_area':
                        self.scorearea_depth = 1
                        self.inscorearea = True
                        for i in range(1,7):
                            self.score[i] = None

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
#print scorelist
for score in scorelist:
    print "曲名   :", score[0]
    print "Light  :", score[1], score[2]
    print "Medium :", score[3], score[4]
    print "Beast  :", score[5], score[6]
