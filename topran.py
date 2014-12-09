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
song_num = 0
l_num = 0
m_num = 0
b_num = 0
l_total = 0
m_total = 0
b_total = 0
lp = 0
lf = 0
lc = 0
lb = 0
mp = 0
mf = 0
mc = 0
mb = 0
bp = 0
bf = 0
bc = 0
bb = 0
ln = 0
mn = 0
bn = 0
for score in scorelist:
    print "曲名   :", score[0]
    print "Light  :", score[1], score[2]
    print "Medium :", score[3], score[4]
    print "Beast  :", score[5], score[6]
    if score[1] != None:
        l_total += int(score[1])
        l_num += 1
    if score[3] != None:
        m_total += int(score[3])
        m_num += 1
    if score[5] != None:
        b_total += int(score[5])
        b_num += 1
    if score[2] != None:
        if score[2] == 'Perfect':
            lp += 1
        if score[2] == 'FullCombo':
            lf += 1
        if score[2] == 'Clear':
            lc += 1
        if score[2] == 'Failed':
            lb += 1
    else:
        ln += 1
    if score[4] != None:
        if score[4] == 'Perfect':
            mp += 1
        if score[4] == 'FullCombo':
            mf += 1
        if score[4] == 'Clear':
            mc += 1
        if score[4] == 'Failed':
            mb += 1
    else:
        mn += 1
    if score[6] != None:
        if score[6] == 'Perfect':
            bp += 1
        if score[6] == 'FullCombo':
            bf += 1
        if score[6] == 'Clear':
            bc += 1
        if score[6] == 'Failed':
            bb += 1
    else:
        bn += 1
    song_num += 1
print "Total Score"
print "Light  :", l_total
print "Medium :", m_total
print "Beast  :", b_total
print "Total  :", l_total + b_total + b_total
print "Average Score"
print "Light  :", l_total / song_num
print "Medium :", m_total / song_num
print "Beast  :", b_total / song_num
print "Average Score(プレイ済み)"
print "Light  :", l_total / l_num
print "Medium :", m_total / m_num
print "Beast  :", b_total / b_num
print "Clear Lanp"
print "Lanp      : Light, Medium, Beast"
print "Perfect   :", lp, ",", mp, ",", bp
print "FullCombo :", lf, ",", mf, ",", bf
print "Clear     :", lc, ",", mc, ",", bc
print "Failed    :", lb, ",", mb, ",", bb
print "NoPlay    :", ln, ",", mn, ",", bn
