# -*- coding: utf-8 -*-

from HTMLParser import HTMLParser
import urllib2

class MyHTMLParser(HTMLParser):
    def __init__(self):
        self.nowtag = ''
        self.nowattr = ''
        self.scorelist = []
        self.title = ''
        self.score = [None] * 4
        self.medal = [None] * 4
        self.inscorearea = False
        self.dif = 0
        HTMLParser.__init__(self)

    def handle_data(self, data):
        if self.nowtag == 'div' or self.nowtag == 'span' or self.nowtag == 'img':
            for name, value in self.nowattr:
                if name == 'class':
                    if value == 'mymusic_tit':
                        self.title += data
                    else:
                        if value == 'score_num':
                            self.score[self.dif] = data
                        if value == 'perfect':
                            self.medal[self.dif] = 3
                        if value == 'fullcombo':
                            self.medal[self.dif] = 2
                        if value == 'clear':
                            self.medal[self.dif] = 1
                        if value == 'failed':
                            self.medal[self.dif] = 0
    
    def handle_starttag(self, tag, attr):
        self.nowtag = tag
        self.nowattr = attr
        if tag == 'div':
            if self.inscorearea:
                self.scorearea_depth += 1
                for name, value in attr:
                    if value == 'light':
                        self.dif = 0
                    if value == 'medium':
                        self.dif = 1
                    if value == 'beast':
                        self.dif = 2
                    if value == 'nightmare':
                        self.dif = 3

            else:
                for name, value in attr:
                    if name == 'class' and value == 'score_area':
                        self.scorearea_depth = 1
                        self.inscorearea = True
                        self.score = [None] * 4
                        self.medal = [None] * 4

    def handle_endtag(self, tag):
        if tag == 'div':
            if self.inscorearea:
                self.scorearea_depth -= 1
                if self.scorearea_depth == 0:
                    for var in range(0, 4):
                        if self.score[var] != None:
                            self.scorelist.append((self.title,var,self.score[var],self.medal[var]))
                    self.inscorearea = False
                    self.title = ''
        if tag == self.nowtag:
            self.nowtag = ''
            self.nowattr = ''

    def get_scorelist(self):
        return self.scorelist

#----------------------Light,Medium,Beast------------------------------
f = open('sample_beast_lmb.html', 'r')
allLines = f.read()
f.close()

parser = MyHTMLParser()
parser.feed(allLines)

scorelist = parser.get_scorelist()

print "曲名,難易度,スコア,メダル"
for score in scorelist:
    print str(score[0]) + "," + str(score[1]) + "," + str(score[2]) + "," + str(score[3])


#----------------------------Nightmare---------------------------------
f1 = open('sample_beast_n.html', 'r')
allLines1 = f1.read()
f1.close()

parser1 = MyHTMLParser()
parser1.feed(allLines1)

scorelist1 = parser1.get_scorelist()

for score in scorelist1:
    print str(score[0]) + "," + str(score[1]) + "," + str(score[2]) + "," + str(score[3])
